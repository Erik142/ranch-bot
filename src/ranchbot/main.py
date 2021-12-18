import os
import sys

from dotenv import load_dotenv
from core.bot import Bot

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


if __name__ == "__main__":
    checkConfigValues()
    bot = Bot(prefix, status)
    bot.loadCommands()
    bot.run(token)
