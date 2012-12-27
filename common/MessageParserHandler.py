class MessageParserHandler:
    """ Override to handle a parsed message. """
    def __init__(self):
        pass

    def handle_message(self, message):
        """ This must be overriden. """
        raise NotImplementedError("MessageParserHandler.handle_message is not implemented")
