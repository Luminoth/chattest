import logging

from Database import Database

class LocalUser:
    def __init__(self, username):
        # init member variables
        self.__username = username
        self.__loggedin = False

    def get_username(self):
        return self.__username

    def set_logged_in(self, loggedin):
        self.__loggedin = loggedin

    def get_logged_in(self):
        return self.__loggedin

class LocalDatabase(Database):
    """ A volatile local user database. """
    def __init__(self):
        Database.__init__(self)

        # get a logger
        self.__logger = logging.getLogger("chattest.server.LocalDatabase")
        self.__logger.debug("Created a new LocalDatabase object...")

        # init member variables
        self.__users = []

    def connect(self):
        self.__logger.info("Using local database...")
        return True

    def authenticate(self, username, password):
        user = self.__find_user(username)
        if(user and user.get_logged_in()):
            self.__logger.error("User is already logged in")
            return False
        elif(user):
            self.__logger.warn("User has returned")
            return True

        self.__users.append(LocalUser(username))
        self.__logger.info("Authentication success")
        return True

    def set_logged_in(self, username, loggedin):
        user = self.__find_user(username)
        if(not user): return False

        user.set_logged_in(loggedin)
        return True

    def get_logged_in(self, username):
        user = self.__find_user(username)
        if(not user): return False

        return user.get_logged_in()

    def __find_user(self, username):
        users = filter(lambda u: u.get_username() == username, self.__users)
        if(not users or len(users) == 0): return None
        return users[0]
