CREATE TABLE IF NOT EXISTS Players (
       discordName TEXT PRIMARY KEY,
       minecraftName TEXT NOT NULL UNIQUE,
       permissionLevel INT NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS PlayerAuthentications (
       id SERIAL,
       discordName TEXT NOT NULL UNIQUE,
       expiration TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP + (30 * INTERVAL '1 minute'),
       PRIMARY KEY (id),
       FOREIGN KEY (discordName) REFERENCES Players(discordName)
);

CREATE TABLE IF NOT EXISTS ProtectedServers (
       name TEXT PRIMARY KEY,
       permissionLevel INT NOT NULL DEFAULT 0
)

CREATE TABLE IF NOT EXISTS AuthenticationRequests(
       id SERIAL PRIMARY KEY,
       minecraftName TEXT NOT NULL,
       handled BOOLEAN NOT NULL DEFAULT FALSE,
       created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
       FOREIGN KEY (minecraftName) REFERENCES Players(minecraftName)
)
