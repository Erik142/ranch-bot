#!/usr/bin/env python3

from dotenv import load_dotenv

import os
from util.log import log

load_dotenv()

token = os.environ.get("TOKEN")
status = os.environ.get("STATUS")
prefix = os.environ.get("PREFIX")
postgresConnectionString = os.environ.get("POSTGRES_CONNECTION_STRING")
rabbitmqConnectionString = os.environ.get("RABBITMQ_CONNECTION_STRING")


class Config:
    __PREFIX = prefix
    __STATUS = status
    __TOKEN = token
    __POSTGRES_CONNECTION_STRING = postgresConnectionString
    __RABBITMQ_CONNECTION_STRING = rabbitmqConnectionString

    __LOGGER = None

    def __init__(self):
        super().__init__()
        self.__LOGGER = log.getLogger(__name__)

    def validate(self) -> bool:
        if self.__TOKEN is None or self.__TOKEN == "":
            self.__LOGGER.critical(
                "The token could not be retrieved from environment variables. Please set the TOKEN environment variable and try again."
            )
            return False

        if self.__STATUS is None or self.__STATUS == "":
            self.__LOGGER.critical(
                "The activity status could not be retrieved from environment variables. Please set the STATUS environment variable and try again."
            )
            return False

        if self.__PREFIX is None or self.__PREFIX == "":
            self.__LOGGER.critical(
                "The command prefix could not be retrieved from environment variables. Please set the PREFIX environment variable and try again."
            )
            return False

        if (
            self.__POSTGRES_CONNECTION_STRING is None
            or self.__POSTGRES_CONNECTION_STRING == ""
        ):
            self.__LOGGER.critical(
                "The postgres connection string could not be retrieved from environment variables. Please set the POSTGRES_CONNECTION_STRING environment variable and try again."
            )
            return False

        if (
            self.__RABBITMQ_CONNECTION_STRING is None
            or self.__RABBITMQ_CONNECTION_STRING == ""
        ):
            self.__LOGGER.critical(
                "The rabbitmq connection string could not be retrieved from environment variables. Please set the RABBITMQ_CONNECTION_STRING environment variable and try again."
            )
            return False

        return True

    def getPostgresConnectionString(self) -> str:
        return self.__POSTGRES_CONNECTION_STRING

    def getRabbitMqConnectionString(self) -> str:
        return self.__RABBITMQ_CONNECTION_STRING

    def getPrefix(self) -> str:
        return self.__PREFIX

    def getStatus(self) -> str:
        return self.__STATUS

    def getToken(self) -> str:
        return self.__TOKEN
