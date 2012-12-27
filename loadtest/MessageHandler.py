import logging

from common.MessageParserHandler import MessageParserHandler

class MessageHandler(MessageParserHandler):
    """ Handles messages. """
    def __init__(self, client):
        MessageParserHandler.__init__(self)

        # get a logger
        self.__logger = logging.getLogger("chattest.loadtest.MessageHandler")
        self.__logger.debug("Created a new MessageHandler object...")

        # init member variables
        self.__client = client

    def handle_message(self, message):
        self.__client.handle_command(message)
