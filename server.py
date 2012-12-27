#! /usr/bin/env python

import sys
import os
import signal
import logging
import logging.config
import asyncore
import time
import gc

from server.Configuration import configuration, ConfigurationError
from server.ChatServer import ChatServer
from server.TelnetServer import TelnetServer
from server.LocalDatabase import LocalDatabase
from server.MySQLDatabase import MySQLDatabase

def initialize_configuration():
    global config
    global configfilename

    configfilename = "server.conf"

    config = configuration()

    print "Reading configuration from " + configfilename + "..."
    ret = config.read(configfilename)
    config.validate()

    return ret

def save_configuration():
    print "Saving configuration to " + configfilename + "..."

    configfile = open(configfilename, "w")
    config.write(configfile)
    configfile.close()

def initialize_logger():
    global logger

    print "Reading logging config from logging.ini..."
    logging.config.fileConfig("logging.ini")

    logger = logging.getLogger("chattest.server")
    logger.info("Server logger initialized!")

def initialize_database():
    global database

    type = config.get_database_type()
    if(type == "local"):
        database = LocalDatabase()
    elif(type == "mysql"):
        database = MySQLDatabase()
    else:
        logger.error("Unknown database type '" + type + "'")
        return False

    return database.connect()

def signal_handler(signum, frame):
    if(signum == signal.SIGHUP):
        logger.info("Caught SIGHUP, restarting...")
        server.restart(database)
        telnet.restart(server)

        logger.info("Running garbage collector...")
        gc.collect()

def initialize_signal_handlers():
    logger.info("Initializing signal handlers...")
    signal.signal(signal.SIGHUP, signal_handler)

def daemonize():
    print "Daemonizing..."

    try:
        # first child
        pid = os.fork()
        if(pid == 0):
            os.setsid()
            #signal.signal(signal.SIGHUP, signal.SIG_IGN)

            # second child
            pid = os.fork()
            if(pid == 0):
                #os.chdir("/")
                #os.umask(0)
                pass
            else:
                os._exit(0)
        else:
            os._exit(0)

        # close parent file descriptors
        try:
            maxfd = os.sysconf("SC_OPEN_MAX")
        except(AttributeError, ValueError):
            print "WARNING: No SC_OPEN_MAX, using 256"
            maxfd = 256

        try:
            for fd in range(0, maxfd):
                os.close(fd)
        except OSError:
            pass

        os.open("/dev/null", os.O_RDONLY)
        os.open("/dev/null", os.O_RDWR)
        os.open("/dev/null", os.O_RDWR)
    except OSError, err:
        print "OS error: " + str(err)

def main():
    global server
    global telnet

    # read the configuration
    try:
        if(not initialize_configuration()):
            print "WARNING: Reading configuration failed"
            save_configuration()
    except ConfigurationError, err:
        logger.critical(str(err))
        sys.exit(1)

    # daemonize
    if(config.get_misc_daemon()):
        daemonize()

    # initialize the logger
    initialize_logger()
    config.dump()

    # connect to the database
    if(not initialize_database()):
        sys.exit(1)

    # create the servers
    server = ChatServer(database)
    telnet = TelnetServer(server)

    # init the signal handlers
    initialize_signal_handlers()

    try:
        logger.info("Entering event loop...")
        asyncore.loop(1)
    except KeyboardInterrupt, err:
        server.quit()
        telnet.quit()

    save_configuration()

    logger.info("Server terminated successfully")

if __name__ == "__main__":
    main()
