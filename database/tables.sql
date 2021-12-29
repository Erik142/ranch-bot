CREATE TABLE IF NOT EXISTS Players (
       discordName TEXT PRIMARY KEY,
       minecraftName TEXT NOT NULL UNIQUE,
       permissionLevel INT NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS PlayerAuthentications (
       discordName TEXT NOT NULL UNIQUE,
       expiration TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP + (30 * INTERVAL '1 minute'),
       PRIMARY KEY (discordName, expiration),
       FOREIGN KEY (discordName) REFERENCES Players(discordName)
);

CREATE TABLE IF NOT EXISTS ProtectedServers (
       name TEXT PRIMARY KEY,
       permissionLevel INT NOT NULL DEFAULT 0
)
