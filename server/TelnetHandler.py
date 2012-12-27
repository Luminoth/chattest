import errno
import logging
import time
import asyncore
import socket
from Queue import Queue

from Client import Client

from telnet.MessageHandler import MessageHandler
from telnet.QuitCommandHandler import QuitCommandHandler
from telnet.RestartCommandHandler import RestartCommandHandler
from telnet.GarbageCollectionCommandHandler import GarbageCollectionCommandHandler
from telnet.DisconnectCommandHandler import DisconnectCommandHandler
from telnet.ClientsCommandHandler import ClientsCommandHandler
from telnet.HelpCommandHandler import HelpCommandHandler

class TelnetHandlerState:
    def __init__(self, server, handler, chatserver):
        # init member variables
        self.server = server
        self.client = Client()
        self.buffer = Queue()
        self.actions = Queue()
        self.current_send = ""
        self.command_handlers = []

        # create the set of command handlers
        self.message_handler = MessageHandler(handler)
        self.command_handlers.append(QuitCommandHandler(handler, chatserver, server))
        self.command_handlers.append(RestartCommandHandler(handler, chatserver, server))
        self.command_handlers.append(GarbageCollectionCommandHandler(handler))
        self.command_handlers.append(DisconnectCommandHandler(handler))
        self.command_handlers.append(ClientsCommandHandler(handler, chatserver))
        self.command_handlers.append(HelpCommandHandler(handler))

    def pop_buffer(self):
        # only pop if we've sent the entire current buffer
        if(len(self.current_send) <= 0):
            self.current_send = self.buffer.get()

    def update_sent(self, sent):
        self.current_send = self.current_send[sent:]
        #time.sleep(1)

class TelnetHandler(asyncore.dispatcher):
    """ Handles a telnet client. """
    def __init__(self, socket, server, chatserver):
        asyncore.dispatcher.__init__(self, socket)

        # get a logger
        self.__logger = logging.getLogger("chattest.server.TelnetHandler")
        self.__logger.debug("Created a new TelnetHandler object...")

        # init member variables
        self.__state = TelnetHandlerState(server, self, chatserver)

        # client must first login
        self.buffer_send("login: ")

    def handle_expt(self):
        self.__logger.warn(self.get_username() + ": handle_expt")
        self.close()

    def handle_read(self):
        again = True
        while(again):
            try:
                command = self.recv(1024)
                self.__handle_command(command.strip())
                again = False
            except socket.error, err:
                if(err[0] == errno.EAGAIN):
                    again = True
                    continue
                self.__logger.warning(self.get_username() + ": read error - " + str(err))

    def writable(self):
        return len(self.__state.current_send) > 0 or (not self.__state.buffer.empty()) or (not self.__state.actions.empty())

    def handle_write(self):
        # handle actions first
        if(not self.__state.actions.empty()):
            self.__handle_actions()
            return

        # handle commands
        while(self.writable()):
            self.__state.pop_buffer()
            self.__state.update_sent(self.send(self.__state.current_send))

    def handle_close(self):
        self.__logger.info(self.get_username() + ": closed connection")
        self.quit()

    def valid(self):
        return self.__state.client.valid()

    def buffer_action(self, action):
        self.__state.actions.put(action)

    def buffer_send(self, command):
        self.__state.buffer.put(command)

    def get_username(self):
        return self.__state.client.get_username()

    def set_username(self, username):
        self.__state.client.set_username(username)

    def disconnect(self):
        self.__logger.info(self.get_username() + ": disconnecting")
        self.send("Goodbye\n")
        self.quit()

    def quit(self):
        self.close()
        self.__state.client.invalidate()

    def __handle_actions(self):
        while(not self.__state.actions.empty()):
            action = self.__state.actions.get()
            if(action == "quit"):
                self.quit()
            elif(action == "disconnect"):
                self.disconnect()
            else:
                self.__logger.warn(self.get_username() + ": invalid action '" + action + "'")

    def __find_command_handler(self, command):
        handlers = filter(lambda h: h.owner(command), self.__state.command_handlers)
        if(not handlers or len(handlers) == 0): return None
        return handlers[0]

    def __handle_command(self, command):
        if(len(command) == 0):
            self.__logger.warn(self.get_username() + ": got an empty command")
            return

        self.__logger.debug(self.get_username() + ": handling command '" + command + "'")

        # find a handler for the command
        # this defaults to the basic message handler
        # if there are valid handlers
        handler = self.__find_command_handler(command)
        if(handler == None):
            self.__state.message_handler.handle(command)
        else:
            handler.handle(command)
