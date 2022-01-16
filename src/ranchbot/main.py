import os
import sys
import logging

from dotenv import load_dotenv

from core.bot import Bot
from core import args
from util.log import log

load_dotenv()

token = os.environ.get("TOKEN")
status = os.environ.get("STATUS")
prefix = os.environ.get("PREFIX")

logger = None


def checkConfigValues():
    if token is None or token == "":
        logger.critical(
            "The token could not be retrieved from environment variables. Please set the TOKEN environment variable and try again."
        )
        sys.exit(-1)

    if status is None or status == "":
        logger.critical(
            "The activity status could not be retrieved from environment variables. Please set the STATUS environment variable and try again."
        )
        sys.exit(-1)

    if prefix is None or prefix == "":
        logger.critical(
            "The command prefix could not be retrieved from environment variables. Please set the PREFIX environment variable and try again."
        )
        sys.exit(-1)


if __name__ == "__main__":
    args = args.getArgsParser()
    if args.debug:
        log.setLogLevel(logging.DEBUG)
    logger = log.getLogger(__name__)
    logger.debug("Debugging messages are enabled!")
    checkConfigValues()
    bot = Bot(token,prefix, status)
    bot.run()
