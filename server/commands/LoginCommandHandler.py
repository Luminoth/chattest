import logging
import md5
import MySQLdb

from CommandHandler import CommandHandler

class LoginCommandHandler(CommandHandler):
    def __init__(self, client, database):
        CommandHandler.__init__(self, "/login", client)

        # get a logger
        self.__logger = logging.getLogger("chattest.server.commands.LoginCommandHandler")
        self.__logger.debug("Created a new LoginCommandHandler object...")

        # init member variables
        self.__database = database

    def requires_login(self):
        return False

    def handle(self, command):
        CommandHandler.handle(self, command)

        # save the username
        user = self.argument.split(";", 1)
        self.client.set_username(user[0])

        # get the password md5
        passwordmd5 = md5.new(user[1])

        # can't re-login
        if(self.__database.get_logged_in(user[0])):
            self.__logger.warn(user[0] + ": trying to re-login")
            self.client.buffer_send("/failed")
            self.client.quit()
            return

        # authenticate the user
        if(self.__database.authenticate(user[0], passwordmd5.hexdigest())):
            self.__database.set_logged_in(user[0], True)
            self.client.set_logged_in(True)
            self.client.broadcast(self.client.get_username() + " has logged in\n")
            self.client.buffer_send("/success")
        else:
            self.client.set_logged_in(False)
            self.client.buffer_send("/failed")
