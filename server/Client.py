import logging

class Client:
    """ A client connected to the system. """
    def __init__(self):
        # get a logger
        self.__logger = logging.getLogger("chattest.server.Client")
        self.__logger.debug("Created a new Client object...")

        # init member variables
        self.__username = None
        self.__valid = True
        self.__loggedin = False

    def valid(self):
        return self.__valid

    def get_username(self):
        if(self.__username): return self.__username
        return "%None%"

    def set_username(self, username):
        self.__username = username

    def set_logged_in(self, loggedin):
        self.__loggedin = loggedin

    def get_logged_in(self):
        return self.__loggedin

    def invalidate(self):
        self.set_username(None)
        self.__valid = False
        self.__loggedin = False
