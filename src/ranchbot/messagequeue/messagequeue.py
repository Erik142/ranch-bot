#!/usr/bin/env python3

import json
import time
import datetime

import pika
from pika.adapters.asyncio_connection import AsyncioConnection

import asyncio

from core.config import Config
from core.database import PostgresDatabase

import discord
from discord.ext import commands

from util.log import log
from util.embed import embed


class MessageQueue:
    __BOT = None
    __PUBLISH_CONNECTION = None
    __CONSUME_CONNECTION = None
    __PUBLISH_CHANNEL = None
    __EXCHANGE = None
    __QUEUE = None
    __URL = None
    __LOGGER = None
    __DATABASE = None

    def __init__(self, connectionString: str, bot: commands.Bot):
        super().__init__()
        self.__LOGGER = log.getLogger(__name__)
        config = Config()
        self.__EXCHANGE = config.getPublishExchange()
        self.__QUEUE = config.getConsumeQueue()
        self.__DATABASE = PostgresDatabase(config.getPostgresConnectionString())
        self.__URL = connectionString
        self.__BOT = bot
        self.__LOGGER.info("Opening RabbitMQ connection...")
        self.__openConnection()

    def __openConnection(self):
        self.__PUBLISH_CONNECTION = AsyncioConnection(
            pika.URLParameters(self.__URL),
            on_open_callback=self.__on_publish_connection_open,
        )
        self.__LOGGER.info("RabbitMQ publish connection created!")

        self.__CONSUME_CONNECTION = AsyncioConnection(
            pika.URLParameters(self.__URL),
            on_open_callback=self.__on_consume_connection_open,
        )
        self.__LOGGER.info("RabbitMQ consume connection created!")

    def __on_publish_connection_open(self, _unused_connection):
        self.__LOGGER.info("RabbitMQ publish connection open!")
        self.__PUBLISH_CONNECTION.channel(
            on_open_callback=self.__on_publish_channel_open
        )

    def __on_consume_connection_open(self, _unused_connection):
        self.__LOGGER.info("RabbitMQ consume connection open!")
        self.__CONSUME_CONNECTION.channel(
            on_open_callback=self.__on_consume_channel_open
        )

    def __on_publish_channel_open(self, channel):
        self.__PUBLISH_CHANNEL = channel

    def __on_consume_channel_open(self, channel):
        self.__CONSUME_CHANNEL = channel
        self.__CONSUME_CHANNEL.basic_consume(self.__QUEUE, self.__messageCallback, True)

    def __messageCallback(self, ch, method, properties, body):
        loop = asyncio.get_running_loop()
        loop.create_task(self.__handleMessageAsync(ch, method, properties, body))

    async def __handleMessageAsync(self, ch, method, properties, body):
        self.__LOGGER.info(" [x] Received %r" % body)

        # TODO: Fetch Minecraft user from the queue message
        jsonBody = json.loads(body)
        command = jsonBody["command"]

        if command != "login":
            return

        minecraftUser = jsonBody["user"]
        discordId = self.__DATABASE.getDiscordId(minecraftUser)
        self.__LOGGER.info("The user's Discord id is: " + discordId)

        # TODO: Send message to user to log them in
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
                if self.__DATABASE.isPlayerAuthenticated(str(user.id)) == False:
                    self.__DATABASE.deletePlayerAuthentication(str(user.id))
                    self.__DATABASE.addPlayerAuthentication(str(user.id))
                    responseEmbed = embed.getBaseEmbed("", discord.Colour.green())
                    responseEmbed.add_field(
                        name="Minecraft login",
                        value="The login request has been approved. You can now join the protected Minecraft servers for the next 30 minutes.",
                    )

                    if "server" in jsonBody:
                        connectCommand = {
                            "command": "connect",
                            "user": minecraftUser,
                            "server": jsonBody["server"],
                        }
                        self.__PUBLISH_CHANNEL.basic_publish(
                            self.__EXCHANGE, "*", json.dumps(connectCommand)
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

    def close(self):
        self.__PUBLISH_CHANNEL.close()
        self.__PUBLISH_CONNECTION.close()
        self.__CONSUME_CHANNEL.close()
        self.__CONSUME_CONNECTION.close()
