import logging

class MessageHandler:
    def __init__(self, client):
        # get a logger
        self.__logger = logging.getLogger("chattest.server.telnet.MessageHandler")
        self.__logger.debug("Created a new MessageHandler object...")

        # init member variables
        self.client = client

    def handle(self, command):
        self.__logger.info("Telnet got message: " + command)
