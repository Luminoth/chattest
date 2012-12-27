import logging
import threading
import time

from Configuration import configuration

class PingThread(threading.Thread):
    """ Pings a client to make sure it's alive """
    def __init__(self, client):
        threading.Thread.__init__(self)

        # get a logger
        self.__logger = logging.getLogger("chattest.server.PingThread")
        self.__logger.debug("Created a new PingThread object...")

        # get a configuration
        self.__configuration = configuration()

        # init member variables
        self.__client = client

    def run(self):
        while(self.__client.valid()):
            sentdiff = time.time() - self.__client.get_ping_sent()
            responsediff = time.time() - self.__client.get_ping_response()

            # calculate each round in case the config changes
            ping = self.__configuration.get_misc_ping() * 60.0
            timeout = self.__configuration.get_misc_timeout() * 60.0

            # figure out what to do
            if(responsediff > timeout):
                self.__logger.info(self.__client.get_username() + ": ping timeout")
                self.__client.buffer_action("disconnect")
            elif(sentdiff > ping):
                self.__client.send_ping()

            time.sleep(1)

        self.__logger.debug("PingThread exiting")
