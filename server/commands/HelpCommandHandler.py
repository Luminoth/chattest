import logging

from CommandHandler import CommandHandler

class HelpCommandHandler(CommandHandler):
    def __init__(self, client):
        CommandHandler.__init__(self, "/help", client)

        # get a logger
        self.__logger = logging.getLogger("chattest.server.commands.HelpCommandHandler")
        self.__logger.debug("Created a new HelpCommandHandler object...")

    def requires_login(self):
        return True

    def handle(self, command):
        CommandHandler.handle(self, command)

        self.client.buffer_send("/help       - Display this help\n")
        self.client.buffer_send("/disconnect - Disconnect from the server\n")
        self.client.buffer_send("/say        - Say something\n")
