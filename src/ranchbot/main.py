import os
import sys
from sys import platform
from pathlib import Path

import discord
from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()

token = os.environ.get("TOKEN")
status = os.environ.get("STATUS")
prefix = os.environ.get("PREFIX")

def checkConfigValues():
    if token is None or token == "":
        print(
            "The token could not be retrieved from environment variables. Please set the TOKEN environment variable and try again."
        )
        sys.exit(-1)

    if status is None or status == "":
        print(
            "The activity status could not be retrieved from environment variables. Please set the STATUS environment variable and try again."
        )
        sys.exit(-1)

    if prefix is None or prefix == "":
        print(
            "The command prefix could not be retrieved from environment variables. Please set the PREFIX environment variable and try again."
        )
        sys.exit(-1)


class App(commands.Bot):
    
    __COGS_BASE_PATH = "./functions"
    __COG_FILE_REGEXP = "**/*.py"

    def __init__(self):
        super().__init__(
            command_prefix=prefix, help_command=None, intents=discord.Intents.default()
        )
        self.__COGS = self.__getCogs()

    def __getCogs(self) -> list[str]:
        pathSeparator = "/"
        if platform == "win32":
            pathSeparator = "\\"
        cogs = list[str]()
        for path in Path(self.__COGS_BASE_PATH).glob(self.__COG_FILE_REGEXP):
            pathStr = str(path)
            if "__init__.py" not in pathStr:
                pathStr = str.removesuffix(pathStr, ".py")
                pathStr = str.replace(pathStr, ".", "")
                pathStr = str.removeprefix(pathStr, pathSeparator)
                pathStr = str.removesuffix(pathStr, pathSeparator)
                pathStr = str.replace(pathStr, pathSeparator, ".")
                cogs.append(pathStr)
        return cogs

    async def on_ready(self):
        print("Bot is ready!")
        await self.change_presence(
            status=discord.Status.online, activity=discord.Game(status)
        )
        for cog in self.__COGS:
            try:
                print(f"Loading cog {cog}")
                self.load_extension(cog)
                print(f"Loaded cog {cog}")
            except Exception as e:
                exc = "{}: {}".format(type(e).__name__, e)
                print("Failed to load cog {}\n{}".format(cog, exc))

if __name__ == "__main__":
    checkConfigValues()
    app = App()
    app.run(token)
