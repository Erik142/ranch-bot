import sys
import logging
import threading

from ranchbot.core.bot import Bot
from ranchbot.core import args
from ranchbot.core.config import Config
from ranchbot.core.database import PostgresDatabase
from ranchbot.messagequeue.messagequeue import MessageQueue
from ranchbot.util.log import log

logger = None

if __name__ == "__main__":
    arguments = args.getArgsParser()
    if arguments.debug:
        log.setLogLevel(logging.DEBUG)
    logger = log.getLogger(__name__)
    logger.debug("Debugging messages are enabled!")
    config = Config()
    if config.validate() == False:
        sys.exit(-1)

    db_thread = None

    try:
        bot = Bot(config.getPrefix(), config.getToken())
        bot.loadCommands()
        database = PostgresDatabase(config.getPostgresConnectionString())
        db_thread = threading.Thread(target=database.listen, args=[bot])
        db_thread.start()
        logger.info("Starting bot...")
        bot.run(config.getToken())
    except (KeyboardInterrupt, SystemExit):
        logger.warn("KeyboardInterrupt triggered")
        bot.close()
        database.close()
        sys.exit(0)