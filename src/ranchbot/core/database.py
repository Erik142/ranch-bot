#!/usr/bin/env python3
import asyncio
import threading
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
    __LISTEN_CONNECTION = None
    __NOTIFICATION_GENERATOR = None
    __CLOSE = False

    def __init__(self, connectionString):
        super().__init__()
        self.__CONNECTION_STRING = connectionString
        self.__LOGGER = log.getLogger(__name__)

    def add_player(self, discord_id, reg_code):
        with psycopg.connect(self.__CONNECTION_STRING) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Players(discordName, registrationCode) VALUES(%s,%s)", (discord_id, reg_code)
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

        try:
            with psycopg.connect(self.__CONNECTION_STRING) as conn:
                with conn.cursor() as cursor:
                    for row in cursor.execute(
                        "SELECT discordName FROM AuthenticatedPlayers"
                    ):
                        authenticatedPlayers.append(row[0])
        except Exception as e:
            self.__LOGGER.error("An error occured while retrieving authenticated players from PostgreSQL: %s", e)
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

        try:
            with psycopg.connect(self.__CONNECTION_STRING) as conn:
                with conn.cursor() as cursor:
                    for row in cursor.execute("SELECT discordName FROM Players"):
                        players.append(row[0])
        except Exception as e:
            self.__LOGGER.error("An error occured while retrieving all players from PostgreSQL: %s", e)

        return players

    def get_minecraft_user(self, discordName) -> str:
        try:
            with psycopg.connect(self.__CONNECTION_STRING) as conn:
                with conn.cursor() as cursor:
                    minecraftUser = cursor.execute(
                        "SELECT minecraftName FROM Players WHERE discordName=%s",
                        [discordName],
                    ).fetchone()[0]

                    return minecraftUser
        except Exception as e:
            self.__LOGGER.error("An error occured while retrieving the Minecraft user name that is mapped to the Discord id %s: %s", discordName, e)

        return ""

    def get_discord_id(self, minecraftName) -> str:
        try:
            with psycopg.connect(self.__CONNECTION_STRING) as conn:
                with conn.cursor() as cursor:
                    discordId = cursor.execute(
                        "SELECT discordName FROM Players WHERE minecraftName=%s",
                        [minecraftName],
                    ).fetchone()[0]

                    return discordId
        except Exception as e:
            self.__LOGGER.error("An error occured while retrieving the Discord id for the Minecraft user with user name %s: %s", minecraftName, e)

        return ""

    def get_reg_code(self, discord_id) -> str:
        try:
            with psycopg.connect(self.__CONNECTION_STRING) as conn:
                with conn.cursor() as cursor:
                    reg_code = cursor.execute(
                        "SELECT registrationCode FROM Players WHERE discordName=%s",
                        [discord_id],
                    ).fetchone()[0]

                    return reg_code
        except Exception as e:
            self.__LOGGER.error("An error occured while retrieving the Discord id for the Minecraft user with user name %s: %s", minecraftName, e)

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
        try:
            with psycopg.connect(self.__CONNECTION_STRING) as conn:
                with conn.cursor() as cursor:
                    minecraftName = cursor.execute(
                        "SELECT minecraftName FROM AuthenticationRequests WHERE id=%s", [id]
                    ).fetchone()[0]
                    return minecraftName
        except Exception as e:
            self.__LOGGER.error("An error occured while retrieving the Minecraft user name for the authentication request with id %s: %s", id, e)
            return ""

    def get_auth_request_server(self, id: int):
        try:
            with psycopg.connect(self.__CONNECTION_STRING) as conn:
                with conn.cursor() as cursor:
                    minecraftServer = cursor.execute(
                        "SELECT minecraftServer FROM AuthenticationRequests WHERE id=%s", [id]
                    ).fetchone()[0]
                    return minecraftServer
        except Exception as e:
            self.__LOGGER.error("An error occured while retrieving the Minecraft server for the authentication request with id %s: %s", id, e)

    def set_auth_request_handled(self, id: int):
        with psycopg.connect(self.__CONNECTION_STRING) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE AuthenticationRequests SET handled=TRUE WHERE id=%s", [id]
                ).fetchone()[0]

    def close(self):
        self.__LISTEN_CONNECTION.close()
        self.__NOTIFICATION_GENERATOR.close()
        self.__CLOSE = True

    def listen(self, bot: Bot):
        self.__BOT = bot
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop = asyncio.get_event_loop()

        while not self.__CLOSE:
            try:
                with psycopg.connect(self.__CONNECTION_STRING, autocommit=True) as conn:
                    self.__LISTEN_CONNECTION = conn
                    conn.execute("LISTEN bot_updates")
                    gen = conn.notifies()
                    self.__NOTIFICATION_GENERATOR = gen

                    for notify in gen:
                        id = notify.payload
                        self.__LOGGER.info(" [x] Received notification with id %r" % id)
                        try:
                            thread = threading.Thread(target=self._handler_threaded, args=[id])
                            thread.start()
                        except:
                            self.__LOGGER.error("An error occured when handling a PostgreSQL notification...")
            except (KeyboardInterrupt, SystemExit):
                return
            except:
                self.__LOGGER.error("An error occured when listening to PostgreSQL notifications. Trying again...")
                time.sleep(10)

    def _handler_threaded(self, id: int):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop = asyncio.get_event_loop()

        loop.run_until_complete(self._handle_notification(id))

    async def _handle_notification(self, id: int):
        self.__LOGGER.info("Starting notification handler for notification with id " + id)
        minecraftUser = self.get_auth_request_user(id)

        # Not a valid authentication request id
        if minecraftUser == "" or minecraftUser is None:
            self.__LOGGER.error("The Minecraft username for the authentication request with id %s could not be found", id)
            return

        discordId = self.get_discord_id(minecraftUser)

        # The Minecraft user is not registered in PostgreSQL
        if discordId == "" or discordId is None:
            self.__LOGGER.error("The Discord ID for the minecraft user with username %s could not be found in PostgreSQL")
            return

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
                try:
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
                except Exception as e:
                    self.__LOGGER.error("An error occured while finalizing the authentication request with id %s: %s", id, e)
                    errorEmbed = embed.getBaseEmbed("", discord.Colour.red())
                    errorEmbed.add_field(
                        name="Minecraft login",
                        value="An error occured while logging you in. Please try again or contact one of the moderators if the issue persists."
                    )
                    try:
                        await user.send(embed=errorEmbed)
                    except Exception as e1:
                        self.__LOGGER.error("Could not send login error message back to the Discord user: %s", e1)
                    return
            elif str(reaction.emoji) == "❌":
                responseEmbed = embed.getBaseEmbed("", discord.Colour.red())
                responseEmbed.add_field(
                    name="Minecraft login",
                    value="The login request has been denied. Contact the Discord moderators if you keep receiving login requests from the Minecraft server.",
                )

        await user.send(embed=responseEmbed)