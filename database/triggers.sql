CREATE OR REPLACE FUNCTION NotifyBot()
    RETURNS trigger AS $$
    BEGIN
        NOTIFY bot_updates, NEW.id
        
        DELETE 
        FROM AuthenticationRequests
        WHERE handled = TRUE and (created + (30 * INTERVAL '1 minute')) > now()::timestamp
    END
    $$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION NotifyMinecraft()
    RETURNS trigger AS $$
    BEGIN

    END
    $$ LANGUAGE plpgsql;

CREATE TRIGGER InsertAuthRequests
    AFTER INSERT ON AuthenticationRequests
    FOR EACH ROW EXECUTE PROCEDURE NotifyBot()

CREATE TRIGGER UpdateAuthRequests
    AFTER INSERT ON PlayerAuthentications
    FOR EACH ROW EXECUTE PROCEDURE NotifyMinecraft()