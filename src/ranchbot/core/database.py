#!/usr/bin/env python3
import psycopg


class PostgresDatabase:
    __CONNECTION_STRING = None

    def __init__(self, connectionString):
        super().__init__()
        self.__CONNECTION_STRING = connectionString

    def addPlayer(self, discordName, minecraftName):
        with psycopg.connect(self.__CONNECTION_STRING) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Players VALUES(%s,%s)", (discordName, minecraftName)
                )

    def addPlayerAuthentication(self, discordName):
        with psycopg.connect(self.__CONNECTION_STRING) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO PlayerAuthentications VALUES(%s)",
                    [discordName],
                )

    def getAuthenticatedPlayers(self) -> list[str]:
        authenticatedPlayers = list(str)

        with psycopg.connect(self.__CONNECTION_STRING) as conn:
            with conn.cursor() as cursor:
                for row in cursor.execute(
                    "SELECT discordName FROM AuthenticatedPlayers"
                ):
                    authenticatedPlayers.append(row[0])

        return authenticatedPlayers

    def isPlayerAuthenticated(self, discordId) -> bool:
        count = 0
        with psycopg.connect(self.__CONNECTION_STRING) as conn:
            with conn.cursor() as cursor:
                count = cursor.execute(
                    "SELECT COUNT(*) FROM AuthenticatedPlayers WHERE discordName=%s",
                    [discordId],
                ).fetchone()[0]

        return count > 0

    def deletePlayerAuthentication(self, discordName):
        with psycopg.connect(self.__CONNECTION_STRING) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM PlayerAuthentications WHERE discordName=%s",
                    [discordName],
                )

    def getPlayers(self) -> list[str]:
        players = list(str)

        with psycopg.connect(self.__CONNECTION_STRING) as conn:
            with conn.cursor() as cursor:
                for row in cursor.execute("SELECT discordName FROM Players"):
                    players.append(row[0])

        return players

    def getMinecraftUser(self, discordName) -> str:
        with psycopg.connect(self.__CONNECTION_STRING) as conn:
            with conn.cursor() as cursor:
                minecraftUser = cursor.execute(
                    "SELECT minecraftName FROM Players WHERE discordName=%s",
                    [discordName],
                ).fetchone()[0]

                return minecraftUser

        return ""

    def getDiscordId(self, minecraftName) -> str:
        with psycopg.connect(self.__CONNECTION_STRING) as conn:
            with conn.cursor() as cursor:
                discordId = cursor.execute(
                    "SELECT discordName FROM Players WHERE minecraftName=%s",
                    [minecraftName],
                ).fetchone()[0]

                return discordId

        return ""

    def isPlayerRegistered(self, discordName) -> bool:
        with psycopg.connect(self.__CONNECTION_STRING) as conn:
            with conn.cursor() as cursor:
                playerCount = cursor.execute(
                    "SELECT COUNT(*) FROM Players WHERE discordName=%s", [discordName]
                ).fetchone()[0]
                return playerCount > 0

    def deletePlayer(self, discordName):
        with psycopg.connect(self.__CONNECTION_STRING) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM Players WHERE discordName=%s", [discordName]
                )
