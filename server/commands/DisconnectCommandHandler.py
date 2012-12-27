import logging

from CommandHandler import CommandHandler

class DisconnectCommandHandler(CommandHandler):
    def __init__(self, client):
        CommandHandler.__init__(self, "/disconnect", client)

        # get a logger
        self.__logger = logging.getLogger("chattest.server.commands.DisconnectCommandHandler")
        self.__logger.debug("Created a new DisconnectCommandHandler object...")

    def requires_login(self):
        return False

    def handle(self, command):
        CommandHandler.handle(self, command)

        if(self.client.get_logged_in()):
            self.client.broadcast(self.client.get_username() + " has disconnected\n")
        self.client.quit()
