import logging

from server.commands.CommandHandler import CommandHandler

class HelpCommandHandler(CommandHandler):
    def __init__(self, client):
        CommandHandler.__init__(self, "/help", client)

        # get a logger
        self.__logger = logging.getLogger("chattest.server.telnet.HelpCommandHandler")
        self.__logger.debug("Created a new HelpCommandHandler object...")

    def requires_login(self):
        return True

    def handle(self, command):
        CommandHandler.handle(self, command)

        self.client.buffer_send("/help       - Display this help\n")
        self.client.buffer_send("/disconnect - Disconnect from the server\n")
        self.client.buffer_send("/clients    - Clients\n")
        self.client.buffer_send("/gc         - Gargabe collector\n")
        self.client.buffer_send("/restart    - Restart the server\n")
        self.client.buffer_send("/quit       - Quit the server\n")
