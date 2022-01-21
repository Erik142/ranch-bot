#!/usr/bin/env python3
import psycopg


class PostgresDatabase:
    __CONNECTION_STRING = None

    def __init__(self, connectionString):
        super().__init__()
        self.__CONNECTION_STRING = connectionString

    def add_player(self, discordName, minecraftName):
        with psycopg.connect(self.__CONNECTION_STRING) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Players VALUES(%s,%s)", (discordName, minecraftName)
                )

    def add_player_auth(self, discordName):
        with psycopg.connect(self.__CONNECTION_STRING) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO PlayerAuthentications VALUES(%s)",
                    [discordName],
                )

    def get_authenticated_players(self) -> list[str]:
        authenticatedPlayers = list(str)

        with psycopg.connect(self.__CONNECTION_STRING) as conn:
            with conn.cursor() as cursor:
                for row in cursor.execute(
                    "SELECT discordName FROM AuthenticatedPlayers"
                ):
                    authenticatedPlayers.append(row[0])

        return authenticatedPlayers

    def is_player_authenticated(self, discordId) -> bool:
        count = 0
        with psycopg.connect(self.__CONNECTION_STRING) as conn:
            with conn.cursor() as cursor:
                count = cursor.execute(
                    "SELECT COUNT(*) FROM AuthenticatedPlayers WHERE discordName=%s",
                    [discordId],
                ).fetchone()[0]

        return count > 0

    def delete_player_auth(self, discordName):
        with psycopg.connect(self.__CONNECTION_STRING) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM PlayerAuthentications WHERE discordName=%s",
                    [discordName],
                )

    def get_players(self) -> list[str]:
        players = list(str)

        with psycopg.connect(self.__CONNECTION_STRING) as conn:
            with conn.cursor() as cursor:
                for row in cursor.execute("SELECT discordName FROM Players"):
                    players.append(row[0])

        return players

    def get_minecraft_user(self, discordName) -> str:
        with psycopg.connect(self.__CONNECTION_STRING) as conn:
            with conn.cursor() as cursor:
                minecraftUser = cursor.execute(
                    "SELECT minecraftName FROM Players WHERE discordName=%s",
                    [discordName],
                ).fetchone()[0]

                return minecraftUser

        return ""

    def get_discord_id(self, minecraftName) -> str:
        with psycopg.connect(self.__CONNECTION_STRING) as conn:
            with conn.cursor() as cursor:
                discordId = cursor.execute(
                    "SELECT discordName FROM Players WHERE minecraftName=%s",
                    [minecraftName],
                ).fetchone()[0]

                return discordId

        return ""

    def is_player_registered(self, discordName) -> bool:
        with psycopg.connect(self.__CONNECTION_STRING) as conn:
            with conn.cursor() as cursor:
                playerCount = cursor.execute(
                    "SELECT COUNT(*) FROM Players WHERE discordName=%s", [discordName]
                ).fetchone()[0]
                return playerCount > 0

    def delete_player(self, discordName):
        with psycopg.connect(self.__CONNECTION_STRING) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM Players WHERE discordName=%s", [discordName]
                )
