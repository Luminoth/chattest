import logging

class MessageGenerator:
    """ Generates a message. """
    def __init__(self):
        self.__logger = logging.getLogger("chattest.common.MessageGenerator")
        self.__logger.debug("Created a new MessageGenerator object...")

    def generate_message(self, message):
        return "<message>" + message + "</message>"
