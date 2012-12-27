import logging

from server.commands.CommandHandler import CommandHandler

class ClientsCommandHandler(CommandHandler):
    def __init__(self, client, server):
        CommandHandler.__init__(self, "/clients", client)

        # get a logger
        self.__logger = logging.getLogger("chattest.server.telnet.ClientsCommandHandler")
        self.__logger.debug("Created a new ClientsCommandHandler object...")

        self.__server = server

    def requires_login(self):
        return True

    def handle(self, command):
        CommandHandler.handle(self, command)

        if(self.argument == "da"):
            self.client.buffer_send("Disconnecting all clients...\n")
            self.__server.disconnect_all()
        elif(self.argument.startswith("d")):
            client = self.argument[2:]
            self.client.buffer_send("Disconnecting client '" + client + "'\n")
        else:
            self.client.buffer_send("Clients: %(clients)d\n" % { "clients": self.__server.client_count() })
