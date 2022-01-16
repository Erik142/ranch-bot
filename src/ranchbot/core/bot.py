#!/usr/bin/env python3
import os
from pathlib import Path
from sys import platform
from asyncio import AbstractEventLoop

import hikari
import hikari.presences
import lightbulb

from util.log import log

bot = lightbulb.BotApp(token="")


class Bot(lightbulb.BotApp):

    __COGS_BASE_PATH = "commands"
    __COG_FILE_REGEXP = "**/*.py"

    __status = ""
    __plugins = []
    __logger = log.getLogger(__name__)

    def __init__(
        self, token: str, prefix: str, status: str, eventLoop: AbstractEventLoop = None
    ):
        if os.name != "nt":
            import uvloop

            uvloop.install()
        super().__init__(token, prefix)
        self.__status = status

    #        self.__cogs = self.__getCogs()

    def __get_plugins(self) -> list[str]:
        pathSeparator = "/"
        if platform == "win32":
            pathSeparator = "\\"
        cogs = list[str]()
        scriptPath = os.path.dirname(os.path.realpath(__file__))
        cogsPath = os.path.join(scriptPath, "../", self.__cogs_BASE_PATH)

        for path in Path(cogsPath).glob(self.__COG_FILE_REGEXP):
            pathStr = str(path)
            if "__init__.py" not in pathStr:
                pathStr = str.removesuffix(pathStr, ".py")
                pathStr = str.replace(pathStr, ".", "")
                pathStr = pathStr[pathStr.find(self.__cogs_BASE_PATH) :]
                self.__logger.debug(pathStr)
                pathStr = str.removeprefix(pathStr, pathSeparator)
                pathStr = str.removesuffix(pathStr, pathSeparator)
                pathStr = str.replace(pathStr, pathSeparator, ".")
                cogs.append(pathStr)
        return cogs

    def load_plugins(self):
        for plugin in self.__plugins:
            try:
                self.__logger.info(f"Loading cog {plugin}")
                self.load_extension(plugin)
                self.__logger.info(f"Loaded cog {plugin}")
            except Exception as e:
                exc = "{}: {}".format(type(e).__name__, e)
                self.__logger.error("Failed to load cog {}\n{}".format(plugin, exc))

    def run(self) -> None:
        self.event_manager.subscribe(hikari.StartedEvent, self.on_started)        
        
        super().run(
            activity=hikari.Activity(
                name=self.__status,
                type=hikari.presences.ActivityType.PLAYING
            )
        )

    async def on_started(self, event: hikari.StartedEvent):
        self.__logger.info("Bot is started!")
        self.load_plugins()