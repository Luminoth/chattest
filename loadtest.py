#! /usr/bin/env python

import sys
import logging
import logging.config
import time
import asyncore

from loadtest.Configuration import configuration
from loadtest.EventHandler import EventHandler

def initialize_logger():
    global logger

    print "Reading logging config from logging.ini..."
    logging.config.fileConfig("logging.ini")

    logger = logging.getLogger("chattest.loadtest")
    logger.info("Load tester logger initialized!")

def initialize_configuration():
    global config
    global configfilename

    configfilename = "loadtest.conf"

    config = configuration()

    logger.info("Reading configuration...")
    ret = config.read(configfilename)

    config.dump()
    return ret

def save_configuration():
    logger.info("Saving configuration to " + configfilename + "...")

    configfile = open(configfilename, "w")
    config.write(configfile)
    configfile.close()

def main():
    global clients

    initialize_logger()

    if(not initialize_configuration()):
        logger.warn("Reading configuration failed")
        save_configuration()

    clients = []
    for i in range(config.get_users_amount()):
        clients.append(EventHandler(i+1))

    try:
        logger.info("Entering event loop...")
        asyncore.loop(1)
    except KeyboardInterrupt, err:
        for i in range(config.get_users_amount()):
            clients[i].disconnect()

    save_configuration()

    logger.info("Load tester terminated successfully")

if __name__ == "__main__":
    main()
