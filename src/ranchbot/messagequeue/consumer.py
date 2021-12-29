#!/usr/bin/env python3

import threading
import pika

from discord.ext import commands

from util.log import log


class MessageQueue(threading.Thread):
    __BOT = None
    __CONNECTION = None
    __CHANNEL = None
    __URL = "amqp://guest:guest@127.0.0.1:5672/%2F"
    __LOGGER = None

    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.__LOGGER = log.getLogger(__name__)
        self.__BOT = bot
        self.__LOGGER.info("Opening RabbitMQ connection...")
        self.__openConnection()

    def __openConnection(self):
        self.__CONNECTION = pika.SelectConnection(
            pika.URLParameters(self.__URL),
            on_open_callback=self.__on_connection_open,
        )
        self.__LOGGER.info("RabbitMQ connection created!")

    def __on_connection_open(self, _unused_connection):
        self.__LOGGER.info("RabbitMQ connection open!")
        self.__CONNECTION.channel(on_open_callback=self.__on_channel_open)

    def __on_channel_open(self, channel):
        self.__CHANNEL = channel
        self.__CHANNEL.basic_consume(
            "minecraft-authentication", self.__messageCallback, True
        )

    def __messageCallback(self, ch, method, properties, body):
        self.__LOGGER.info(" [x] Received %r" % body)

    def close(self):
        self.__CONNECTION.close()
        self.__CONNECTION.close()
        self.__CONNECTION.ioloop.stop()

    def run(self):
        self.__CONNECTION.ioloop.start()
