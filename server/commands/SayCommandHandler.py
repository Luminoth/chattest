import logging

from CommandHandler import CommandHandler

class SayCommandHandler(CommandHandler):
    def __init__(self, client):
        CommandHandler.__init__(self, "/say", client)

        # get a logger
        self.__logger = logging.getLogger("chattest.server.commands.SayCommandHandler")
        self.__logger.debug("Created a new SayCommandHandler object...")

    def requires_login(self):
        return True

    def handle(self, command):
        CommandHandler.handle(self, command)

        self.client.update_ping(False)
        self.client.broadcast(self.client.get_username() + ": " + self.argument + "\n")
