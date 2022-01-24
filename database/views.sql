CREATE OR REPLACE VIEW AuthenticatedPlayers AS
       SELECT id, authRequestId, discordName, minecraftName
       FROM Players
       INNER JOIN PLayerAuthentications USING (discordName)
       WHERE expiration >= now()::timestamp;