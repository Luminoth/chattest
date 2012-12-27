import logging

from server.commands.CommandHandler import CommandHandler

class QuitCommandHandler(CommandHandler):
    def __init__(self, client, server, telnet):
        CommandHandler.__init__(self, "/quit", client)

        # get a logger
        self.__logger = logging.getLogger("chattest.server.telnet.QuitCommandHandler")
        self.__logger.debug("Created a new QuitCommandHandler object...")

        # init member variables
        self.__server = server
        self.__telnet = telnet

    def requires_login(self):
        return True

    def handle(self, command):
        CommandHandler.handle(self, command)

        self.__server.quit()
        self.__telnet.quit()
