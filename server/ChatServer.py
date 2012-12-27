import logging
import asyncore
import socket
from Queue import Queue

from Configuration import configuration
from ClientHandler import ClientHandler

class ChatServer(asyncore.dispatcher):
    """ The main server dispatcher """
    def __init__(self, database):
        asyncore.dispatcher.__init__(self)

        # get a logger
        self.__logger = logging.getLogger("chattest.server.ChatServer")
        self.__logger.debug("Created a new ChatServer object...")

        self.__initialize(database)

    def restart(self, database):
        self.__logger.info("Chat server restarting...")
        self.quit()
        self.__initialize(database)

    def handle_accept(self):
        self.__logger.info("Chat server accepting new connection...")
        self.__clients.append(ClientHandler(self.accept()[0], self, self.__database))

    def writable(self):
        # remove all the invalid clients
        blen = len(self.__clients)
        self.__clients = filter(lambda c: c.valid(), self.__clients)
        alen = len(self.__clients)

        if(alen != blen): self.__logger.info("Chat server removed %(count)d invalid clients" % { "count": blen - alen })

    def broadcast(self, command):
        self.__logger.debug("Chat server broadcasting '" + command + "'")
        map(lambda c: c.buffer_send(command), self.__clients)

    def find_client(self, username):
        self.__logger.debug("Chat server finding '" + username + "'")
        clients = filter(lambda c: c.get_username() == username, self.__clients)
        if(not clients or len(clients) == 0 or (not clients[0].valid())): return None
        return clients[0]

    def disconnect(self, username):
        client = self.find_client(username)
        if(not client):
            self.__logger.warn("Chat server can't disconnect '" + username + "'")
            return

        # disconnect the client
        self.__logger.info("Chat server disconnecting '" + username + "'")
        client.disconnect()

    def disconnect_all(self):
        self.__logger.info("Chat server disconnecting %(count)d clients..." % { "count": self.client_count() })
        map(lambda c: c.disconnect(), self.__clients)
        self.__clients = []

    def quit(self):
        self.__logger.info("Chat server quiting...")
        self.disconnect_all()
        self.close()

    def client_count(self):
        return len(filter(lambda c: c.valid(), self.__clients))

    def get_database(self):
        return self.__database

    def __initialize(self, database):
        self.__logger.info("Chat server initializing...")

        # get a configuration
        self.__configuration = configuration()

        # init member variables
        self.__database = database
        self.__clients = []

        self.__create_socket()

    def __create_socket(self):
        self.__logger.info("Chat server creating socket...")
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()

        self.__logger.info("Chat server binding to port %(port)d" % { "port": self.__configuration.get_network_port() })
        self.bind(("", self.__configuration.get_network_port()))
        self.listen(5)
