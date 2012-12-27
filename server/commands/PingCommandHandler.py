import logging

from CommandHandler import CommandHandler

class PingCommandHandler(CommandHandler):
    def __init__(self, client):
        CommandHandler.__init__(self, "/ping", client)

        # get a logger
        self.__logger = logging.getLogger("chattest.server.commands.PingCommandHandler")
        self.__logger.debug("Created a new PingCommandHandler object...")

    def requires_login(self):
        return False

    def handle(self, command):
        CommandHandler.handle(self, command)

        self.client.update_ping()
