import asyncio
import os
import sys
import logging

from dotenv import load_dotenv

from ranchbot.core.bot import Bot
from ranchbot.core import args
from ranchbot.core.config import Config
from ranchbot.core.database import PostgresDatabase
from ranchbot.messagequeue.messagequeue import MessageQueue
from ranchbot.util.log import log

logger = None


if __name__ == "__main__":
    args = args.getArgsParser()
    if args.debug:
        log.setLogLevel(logging.DEBUG)
    logger = log.getLogger(__name__)
    logger.debug("Debugging messages are enabled!")
    config = Config()
    if config.validate() == False:
        sys.exit(-1)

    try:
        bot = Bot(config.getPrefix(), config.getStatus())
        bot.loadCommands()
        database = PostgresDatabase(config.getPostgresConnectionString())
        loop = asyncio.get_event_loop()
        loop.create_task(database.listen(bot))
        # queueConsumer = MessageQueue(config.getRabbitMqConnectionString(), bot)
        bot.run(config.getToken())
    except (KeyboardInterrupt, SystemExit):
        logger.warn("KeyboardInterrupt triggered")
        # queueConsumer.close()
