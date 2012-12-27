#! /usr/bin/env python

import sys
import logging
import logging.config

from wxPython.wx import *

from client.Configuration import configuration
from client.ChatFrame import ChatFrame

def initialize_logger():
    global logger

    print "Reading logging config from logging.ini..."
    logging.config.fileConfig("logging.ini")

    logger = logging.getLogger("chattest.client")
    logger.info("Client logger initialized!")

def initialize_configuration():
    global config
    global configfilename

    configfilename = "client.conf"

    config = configuration()

    logger.info("Reading configuration...")
    config.read(configfilename)

def save_configuration():
    logger.info("Saving configuration to " + configfilename + "...")

    configfile = open(configfilename, "w")
    config.write(configfile)
    configfile.close()

def main():
    initialize_logger()
    initialize_configuration()

    app = wxPySimpleApp()
    frame = ChatFrame(None, -1, "Client", wxSize(500, 300))
    frame.Show(True)
    app.MainLoop()

    save_configuration()

if __name__ == "__main__":
    main()
