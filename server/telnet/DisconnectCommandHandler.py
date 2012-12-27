import logging

from server.commands.CommandHandler import CommandHandler

class DisconnectCommandHandler(CommandHandler):
    def __init__(self, client):
        CommandHandler.__init__(self, "/disconnect", client)

        # get a logger
        self.__logger = logging.getLogger("chattest.server.telnet.DisconnectCommandHandler")
        self.__logger.debug("Created a new DisconnectCommandHandler object...")

    def requires_login(self):
        return True

    def handle(self, command):
        CommandHandler.handle(self, command)

        self.client.quit()
