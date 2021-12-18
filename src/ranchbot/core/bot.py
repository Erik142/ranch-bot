#!/usr/bin/env python3
import os
from pathlib import Path
from sys import platform
from asyncio import AbstractEventLoop

import discord
from discord.ext import commands


class Bot(commands.Bot):

    __COGS_BASE_PATH = "commands"
    __COG_FILE_REGEXP = "**/*.py"

    __STATUS = ""

    def __init__(self, prefix: str, status: str, eventLoop: AbstractEventLoop = None):
        intents = discord.Intents.default()

        if eventLoop == None:
            super().__init__(
                command_prefix=prefix,
                help_command=None,
                intents=intents,
                loop=eventLoop,
            )
        else:
            intents.members = True
            super().__init__(
                command_prefix=prefix,
                help_command=None,
                intents=intents,
            )
        self.__STATUS = status
        self.__COGS = self.__getCogs()

    def __getCogs(self) -> list[str]:
        pathSeparator = "/"
        if platform == "win32":
            pathSeparator = "\\"
        cogs = list[str]()
        scriptPath = os.path.dirname(os.path.realpath(__file__))
        cogsPath = os.path.join(scriptPath, "../", self.__COGS_BASE_PATH)

        for path in Path(cogsPath).glob(self.__COG_FILE_REGEXP):
            pathStr = str(path)
            if "__init__.py" not in pathStr:
                pathStr = str.removesuffix(pathStr, ".py")
                pathStr = str.replace(pathStr, ".", "")
                pathStr = pathStr[pathStr.find(self.__COGS_BASE_PATH) :]
                print(pathStr)
                pathStr = str.removeprefix(pathStr, pathSeparator)
                pathStr = str.removesuffix(pathStr, pathSeparator)
                pathStr = str.replace(pathStr, pathSeparator, ".")
                cogs.append(pathStr)
        return cogs

    def loadCommands(self):
        for cog in self.__COGS:
            try:
                print(f"Loading cog {cog}")
                self.load_extension(cog)
                print(f"Loaded cog {cog}")
            except Exception as e:
                exc = "{}: {}".format(type(e).__name__, e)
                print("Failed to load cog {}\n{}".format(cog, exc))

    async def on_ready(self):
        print("Bot is ready!")
        await self.change_presence(
            status=discord.Status.online, activity=discord.Game(self.__STATUS)
        )