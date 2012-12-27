import os
import errno
import logging
import time
import socket
import asyncore
from xml.sax import SAXException, make_parser
from Queue import Queue

from common.MessageGenerator import MessageGenerator
from common.MessageParser import MessageParser, MessageParserError

from Client import Client
from PingThread import PingThread
from MessageHandler import MessageHandler

class ClientHandlerState:
    def __init__(self, server, database, handler):
        # init member variables
        self.server = server
        self.database = database
        self.client = Client()
        self.buffer = Queue()
        self.actions = Queue()
        self.current_send = ""
        self.ping_sent = 0.0
        self.ping_response = 0.0

    def pop_buffer(self):
        # only pop if we've sent the entire current buffer
        if(len(self.current_send) <= 0):
            self.current_send = self.buffer.get()

    def update_sent(self, sent):
        self.current_send = self.current_send[sent:]
        #time.sleep(1)

class ClientHandler(asyncore.dispatcher):
    """ Handles client connections. """
    def __init__(self, socket, server, database):
        asyncore.dispatcher.__init__(self, socket)

        # get a logger
        self.__logger = logging.getLogger("chattest.server.ClientHandler")
        self.__logger.debug("Created a new ClientHandler object...")

        # init member variables
        self.__state = ClientHandlerState(server, database, self)
        self.__ping_thread = PingThread(self)
        self.__message_generator = MessageGenerator()
        self.__message_parser = make_parser()
        self.__message_parser.setContentHandler(MessageParser(MessageHandler(self, database)))

        # client must first login
        self.buffer_send("/login")

        # start the ping thread
        self.update_ping(False)
        self.__ping_thread.start()

    def handle_expt(self):
        self.__logger.warn(self.get_username() + ": handle_expt")
        self.close()

    def handle_read(self):
        again = True
        while(again):
            try:
                command = self.recv(1024)
                self.__message_parser.feed(command)
                again = False
            except socket.error, err:
                if(err[0] == errno.EAGAIN):
                    again = True
                    continue

                self.__logger.warn(self.get_username() + ": read error - " + str(err))
                self.disconnect(False)
                break
            except SAXException, err:
                self.__logger.warn(self.get_username() + ": parse error - " + str(err))
                self.disconnect()
                break
            except MessageParserError, err:
                self.__logger.warn(self.get_username() + ": parse error - " + str(err))
                self.disconnect()
                break

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
            self.__logger.debug(self.get_username() + ": sending '" + self.__state.current_send + "'")

            try:
                self.__state.update_sent(self.send(self.__state.current_send))
            except socket.error, err:
                self.__logger.warn(self.get_username() + ": send error - " + str(err))
                self.disconnect(False)
                break

    def handle_close(self):
        self.__logger.info(self.get_username() + ": closed connection")
        self.quit()

    def valid(self):
        return self.__state.client.valid()

    def buffer_action(self, action):
        self.__state.actions.put(action)

    def buffer_send(self, command):
        self.__state.buffer.put(self.__message_generator.generate_message(command))

    def broadcast(self, command):
        self.__state.server.broadcast(command)

    def send_ping(self):
        self.__logger.info(self.get_username() + ": sending ping request")
        self.buffer_send("/ping")
        self.__state.ping_sent = time.time()

    def update_ping(self, received=True):
        if(received): self.__logger.info(self.get_username() + ": got ping response")
        else: self.__logger.info(self.get_username() + ": updating ping time")
        self.__state.ping_response = time.time()

    def get_username(self):
        return self.__state.client.get_username()

    def set_username(self, username):
        self.__state.client.set_username(username)

    def get_logged_in(self):
        return self.__state.client.get_logged_in()

    def set_logged_in(self, loggedin):
        return self.__state.client.set_logged_in(loggedin)

    def get_ping_sent(self):
        return self.__state.ping_sent

    def get_ping_response(self):
        return self.__state.ping_response

    def disconnect(self, send=True):
        self.__logger.info(self.get_username() + ": disconnecting")

        if(send):
            self.__logger.debug(self.get_username() + ": sending disconnect message")
            try:
                self.send(self.__message_generator.generate_message("/disconnect"))
            except socket.error, err:
                self.__logger.warn(self.get_username() + ": send error - " + str(err))

        self.quit()

    def quit(self):
        self.close()
        self.__state.database.set_logged_in(self.get_username(), False)
        self.__state.client.invalidate()
        self.__ping_thread.join()

    def __handle_actions(self):
        while(not self.__state.actions.empty()):
            action = self.__state.actions.get()
            if(action == "quit"):
                self.quit()
            elif(action == "disconnect"):
                self.disconnect()
            else:
                self.__logger.warn(self.get_username() + ": invalid action '" + action + "'")
