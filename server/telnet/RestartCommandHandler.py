import logging

from server.commands.CommandHandler import CommandHandler

class RestartCommandHandler(CommandHandler):
    def __init__(self, client, server, telnet):
        CommandHandler.__init__(self, "/restart", client)

        # get a logger
        self.__logger = logging.getLogger("chattest.server.telnet.RestartCommandHandler")
        self.__logger.debug("Created a new RestartCommandHandler object...")

        # init member variables
        self.__server = server
        self.__telnet = telnet

    def requires_login(self):
        return True

    def handle(self, command):
        CommandHandler.handle(self, command)

        self.__server.restart(self.__server.get_database())
        self.__telnet.restart(self.__server)
