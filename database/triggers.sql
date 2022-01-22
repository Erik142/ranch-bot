CREATE OR REPLACE FUNCTION NotifyBot()
    RETURNS trigger AS $$
    BEGIN
        PERFORM pg_notify(CAST('bot_updates' AS TEXT), CAST(NEW.id AS TEXT));
        
        DELETE 
        FROM AuthenticationRequests
        WHERE handled = TRUE and (created + (30 * INTERVAL '1 minute')) > now()::timestamp;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION NotifyMinecraft()
    RETURNS trigger AS $$
    BEGIN
        PERFORM pg_notify(CAST('approved_auths' AS TEXT), CAST(NEW.id AS TEXT));
        RETURN OLD;
    END;
    $$ LANGUAGE plpgsql;

CREATE TRIGGER InsertAuthRequests
    AFTER INSERT ON AuthenticationRequests
    FOR EACH ROW EXECUTE PROCEDURE NotifyBot();

CREATE TRIGGER UpdateAuthRequests
    AFTER INSERT ON PlayerAuthentications
    FOR EACH ROW EXECUTE PROCEDURE NotifyMinecraft();