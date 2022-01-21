#!/usr/bin/env python3
import asyncio
import discord
import psycopg

import select
import time

from ranchbot.core.bot import Bot
from ranchbot.util.log import log
import ranchbot.util.embed.embed as embed


class PostgresDatabase:
    __CONNECTION_STRING = None
    __LOGGER = None

    def __init__(self, connectionString):
        super().__init__()
        self.__CONNECTION_STRING = connectionString
        self.__LOGGER = log.getLogger(__name__)

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
                    "INSERT INTO PlayerAuthentications(discordName) VALUES(%s)",
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

    def get_auth_request_user(self, id) -> str:
        with psycopg.connect(self.__CONNECTION_STRING) as conn:
            with conn.cursor() as cursor:
                minecraftName = cursor.execute(
                    "SELECT minecraftName FROM AuthenticationRequests WHERE id=%s", [id]
                ).fetchone()[0]
                return minecraftName

    def get_auth_request_server(self, id: int):
        with psycopg.connect(self.__CONNECTION_STRING) as conn:
            with conn.cursor() as cursor:
                minecraftServer = cursor.execute(
                    "SELECT minecraftServer FROM AuthenticationRequests WHERE id=%s", [id]
                ).fetchone()[0]
                return minecraftServer

    def set_auth_request_handled(self, id: int):
        with psycopg.connect(self.__CONNECTION_STRING) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE AuthenticationRequests SET handled=TRUE WHERE id=%s", [id]
                ).fetchone()[0]

    def listen(self, bot: Bot):
        self.__BOT = bot

        while True:
            try:
                with psycopg.connect(self.__CONNECTION_STRING, autocommit=True) as conn:
                    conn.execute("LISTEN bot_updates")
                    gen = conn.notifies()

                    for notify in gen:
                        id = notify.payload
                        loop = asyncio.get_running_loop()
                        loop.create_task(self._handle_notification(id))
            except:
                self.__LOGGER.error("An error occured when listening to PostgreSQL notifications. Trying again...")
                time.sleep(10)

    async def _handle_notification(self, id: int):
        self.__LOGGER.info(" [x] Received notification with id %r" % id)

        discordId = self.get_auth_request_user(id)
        minecraftUser = self.get_minecraft_user(discordId)
        self.__LOGGER.info("The user's Discord id is: " + discordId)

        user = await self.__BOT.fetch_user(int(discordId))

        loginEmbed = embed.getBaseEmbed("", discord.Colour.blue())
        loginEmbed.add_field(
            name="Minecraft login",
            value="The Minecraft user "
            + minecraftUser
            + " tried to login on the Discord server. Was it you?",
        )

        message = await user.send(embed=loginEmbed)
        await message.add_reaction("✅")
        await message.add_reaction("❌")

        responseEmbed = None
        reaction = None

        startTime = time.time()

        while reaction is None:
            currentTime = time.time()
            elapsed = currentTime - startTime

            if elapsed > 60:
                break

            message = await user.fetch_message(message.id)

            for r in message.reactions:
                if r.count == 2:
                    reaction = r
                    break

            time.sleep(0.5)

        for r in message.reactions:
            self.__LOGGER.info(
                "Reaction with emoji "
                + str(r.emoji)
                + " has "
                + str(r.count)
                + " reactions."
            )

        if reaction is None:
            self.__LOGGER.info("The login request timed out")
            responseEmbed = embed.getBaseEmbed("", discord.Colour.red())
            responseEmbed.add_field(
                name="Minecraft login",
                value="The login request timed out and has been denied.",
            )
        else:
            self.__LOGGER.info("The user responded with " + str(reaction.emoji))
            if str(reaction.emoji) == "✅":
                if self.__DATABASE.is_player_authenticated(str(user.id)) == False:
                    self.__DATABASE.delete_player_auth(str(user.id))
                    self.__DATABASE.add_player_auth(str(user.id), id)
                    responseEmbed = embed.getBaseEmbed("", discord.Colour.green())
                    responseEmbed.add_field(
                        name="Minecraft login",
                        value="The login request has been approved. You can now join the protected Minecraft servers for the next 30 minutes.",
                    )
                else:
                    responseEmbed = embed.getBaseEmbed("", discord.Colour.red())
                    responseEmbed.add_field(
                        name="Minecraft login",
                        value="You are already logged into the Minecraft server.",
                    )

            elif str(reaction.emoji) == "❌":
                responseEmbed = embed.getBaseEmbed("", discord.Colour.red())
                responseEmbed.add_field(
                    name="Minecraft login",
                    value="The login request has been denied. Contact the Discord moderators if you keep receiving login requests from the Minecraft server.",
                )

        await user.send(embed=responseEmbed)