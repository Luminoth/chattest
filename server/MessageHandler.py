import logging

from common.MessageParserHandler import MessageParserHandler

from commands.DisconnectCommandHandler import DisconnectCommandHandler
from commands.HelpCommandHandler import HelpCommandHandler
from commands.LoginCommandHandler import LoginCommandHandler
from commands.PingCommandHandler import PingCommandHandler
from commands.SayCommandHandler import SayCommandHandler

class MessageHandler(MessageParserHandler):
    """ Handles messages. """
    def __init__(self, server, database):
        MessageParserHandler.__init__(self)

        # get a logger
        self.__logger = logging.getLogger("chattest.server.MessageHandler")
        self.__logger.debug("Created a new MessageHandler object...")

        # init member variables
        self.__server = server
        self.__database = database
        self.__command_handlers = []

        # create the set of command handlers
        self.__command_handlers.append(DisconnectCommandHandler(self.__server))
        self.__command_handlers.append(HelpCommandHandler(self.__server))
        self.__command_handlers.append(LoginCommandHandler(self.__server, database))
        self.__command_handlers.append(PingCommandHandler(self.__server))
        self.__say_handler = SayCommandHandler(self.__server)
        self.__command_handlers.append(self.__say_handler)

    def handle_message(self, message):
        self.__handle_command(message)

    def __find_command_handler(self, command):
        handlers = filter(lambda h: h.owner(command), self.__command_handlers)
        if(not handlers or len(handlers) == 0): return None
        return handlers[0]

    def __handle_command(self, command):
        if(len(command) == 0):
            self.__logger.warn(self.__server.get_username() + ": got an empty command")
            return

        self.__logger.debug(self.__server.get_username() + ": handling command '" + command + "'")

        # find a handler for the command
        # this defaults to the basic message handler
        # if there are valid handlers
        handler = self.__find_command_handler(command)
        if(handler == None):
            if(self.__database.get_logged_in(self.__server.get_username())):
                self.__say_handler.handle(command)
            else:
                self.__handle_notloggedin_message(command)
        elif(handler.requires_login() and not self.__database.get_logged_in(self.__server.get_username())):
            self.__handle_notloggedin_message(command)
        else:
            handler.handle(command)

    def __handle_notloggedin_message(self, command):
        self.__logger.warn(self.__server.get_username() + ": sending messages without logging in '" + command + "'")
        self.__server.buffer_send("/login")
