import logging
import MySQLdb

from Configuration import configuration
from Database import Database

class MySQLDatabase(Database):
    """ Uses a MySQL database to manage users. """
    def __init__(self):
        Database.__init__(self)

        # get a logger
        self.__logger = logging.getLogger("chattest.server.MySQLDatabase")
        self.__logger.debug("Created a new MySQLDatabase object...")

        # get a configuration
        self.__configuration = configuration()

        # init member variables
        self.__connection = None
        self.__cursor = None

    def connect(self):
        self.__logger.info("Connecting to MySQL database...")
        try:
            host = self.__configuration.get_database_host()
            database = self.__configuration.get_database_database()
            user = self.__configuration.get_database_user()
            password = self.__configuration.get_database_password()

            self.__connection = MySQLdb.connect(host=host, db=database, user=user, passwd=password)
            self.__cursor = self.__connection.cursor()
        except MySQLdb.OperationalError, err:
            self.__logger.error("MySQL database error: " + str(err))
            return False

        return True

    def disconnect(self):
        if(self.__cursor): self.__cursor.close()
        if(self.__connection):
            self.__logger.info("Closing MySQL database connection")
            self.__connection.close()

    def authenticate(self, username, password):
        try:
            self.__logger.info("Authenticating " + username + " with passwordmd5 " + password)
            self.__cursor.execute("select * from accounts where username='" + username + "' and passwordmd5='" + password + "'")
        except MySQLdb.OperationalError, err:
            self.__logger.error("MySQL database error: " + str(err))
            return False

        # if we got results, the password is good
        results = self.__cursor.fetchall()
        if(len(results) <= 0):
            self.__logger.info("Authentication failed")
            return False

        # verify can_login and valid
        if(results[0][4] != "Y" or results[0][5] != "Y"):
            self.__logger.info("User is not allowed to login")
            return False

        self.__logger.info("Authentication success")
        return True

    def set_logged_in(self, username, loggedin):
        try:
            if(loggedin):
                self.__logger.info("Marking " + username + " as logged in")
                self.__cursor.execute("update accounts set loggedin='Y' where username='" + username + "'");
            else:
                self.__logger.info("Marking " + username + " as not logged in")
                self.__cursor.execute("update accounts set loggedin='N' where username='" + username + "'");
        except MySQLdb.OperationalError, err:
            self.__logger.error("MySQL database error: " + str(err))
            return False

        return True

    def get_logged_in(self, username):
        try:
            self.__cursor.execute("select loggedin from accounts where username='" + username + "'");
        except MySQLdb.OperationalError, err:
            self.__logger.error("MySQL database error: " + str(err))
            return False

        results = self.__cursor.fetchall()
        if(len(results) <= 0):
            self.__logger.warn("No loggedin results found for " + username)
            return False

        return results[0][0] == 'Y'
