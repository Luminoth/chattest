import logging
import asyncore
import socket
from Queue import Queue

from Configuration import configuration
from TelnetHandler import TelnetHandler

class TelnetServer(asyncore.dispatcher):
    """ The main telnet dispatcher. """
    def __init__(self, server):
        asyncore.dispatcher.__init__(self)

        # get a logger
        self.__logger = logging.getLogger("chattest.server.TelnetServer")
        self.__logger.debug("Created a new TelnetServer object...")

        self.__initialize(server)

    def restart(self, server):
        self.__logger.info("Telnet server restarting...")
        self.quit()
        self.__initialize(server)

    def handle_accept(self):
        self.__logger.info("Telnet server accepting new connection...")
        self.__clients.append(TelnetHandler(self.accept()[0], self, self.__server))

    def writable(self):
        # remove all the invalid clients
        blen = len(self.__clients)
        self.__clients = filter(lambda c: c.valid(), self.__clients)
        alen = len(self.__clients)

        if(alen != blen): self.__logger.info("Telnet server removed %(count)d invalid clients" % { "count": blen - alen })

    def disconnect_all(self):
        self.__logger.info("Telnet server disconnecting %(count)d clients..." % { "count": self.client_count() })
        map(lambda c: c.disconnect(), self.__clients)
        self.__clients = []

    def quit(self):
        self.__logger.info("Telnet server quiting...")
        self.disconnect_all()
        self.close()

    def client_count(self):
        return len(filter(lambda c: c.valid(), self.__clients))

    def __initialize(self, server):
        # get a configuration
        self.__configuration = configuration()

        # init member variables
        self.__server = server
        self.__clients = []

        self.__create_socket()

    def __create_socket(self):
        self.__logger.info("Telnet server creating socket...")
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()

        self.__logger.info("Telnet server binding to port %(port)d" % { "port": self.__configuration.get_telnet_port() })
        self.bind(("", self.__configuration.get_telnet_port()))
        self.listen(5)
