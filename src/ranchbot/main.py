import os
import sys
import logging

from core.bot import Bot
from core import args
from core.config import Config
from messagequeue.consumer import MessageQueue
from util.log import log

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
        queueConsumer = MessageQueue(config.getRabbitMqConnectionString(), bot)
        bot.run(config.getToken())
    except (KeyboardInterrupt, SystemExit):
        logger.warn("KeyboardInterrupt triggered")
        queueConsumer.close()
