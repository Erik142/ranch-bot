CREATE OR REPLACE VIEW AuthenticatedPlayers AS
       SELECT id, authRequestId, discordName, minecraftName
       FROM Players
       INNER JOIN PLayerAuthentications USING (discordName)
       WHERE expiration >= now()::timestamp;

CREATE OR REPLACE VIEW PlayerServerAccess AS
       WITH
       Server AS (
            SELECT name, permissionLevel
            FROM ProtectedServers
       )
       SELECT discordName, minecraftName, Server.name AS serverName
       FROM Players
       NATURAL LEFT OUTER JOIN Server
       WHERE Players.permissionLevel >= Server.permissionLevel;
