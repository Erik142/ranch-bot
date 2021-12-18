#!/usr/bin/env python3

import logging

loggers = dict()
logLevel = logging.INFO


def setLogLevel(level: int):
    global logLevel
    logLevel = level


def getLogger(name: str) -> logging.Logger:
    if name not in loggers.keys():
        logging.basicConfig(level=logLevel)
        logger = logging.getLogger(name)
        logger.setLevel(logLevel)
        loggers[name] = logger

    return loggers[name]
