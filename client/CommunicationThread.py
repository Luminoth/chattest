import logging
import asyncore
import socket
import threading
from xml.sax import SAXException, make_parser
from Queue import Queue

from common.MessageGenerator import MessageGenerator
from common.MessageParser import MessageParser, MessageParserError

from MessageHandler import MessageHandler

class CommunicationThread(asyncore.dispatcher, threading.Thread):
    def __init__(self, server, user, window):
        asyncore.dispatcher.__init__(self)
        threading.Thread.__init__(self)

        # get a logger
        self.__logger = logging.getLogger("chattest.client.CommunicationThread")
        self.__logger.debug("Created a new CommunicationThread object...")

        # init member variables
        self.__server = server
        self.__user = user
        self.__window = window
        self.__connected = False
        self.__message_generator = MessageGenerator()
        self.__message_parser = make_parser()
        self.__message_parser.setContentHandler(MessageParser(MessageHandler(self)))
        self.__actions = Queue()
        self.__buffer = Queue()
        self.__current_send = ""

    def run(self):
        # create the socket
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)

        # connect to the server
        self.__logger.info("Connecting to %(host)s:%(port)d as '%(name)s'..." % { "host": self.__server[0], "port": self.__server[1], "name": self.__user[0] })
        self.connect(self.__server)

        asyncore.loop(1)

    def handle_connect(self):
        pass

    def handle_expt(self):
        self.__logger.warn("handle_expt")
        self.__quit()

    def handle_read(self):
        try:
            data = self.recv(1024)
            if(len(data) == 0):
                return

            if(data.startswith("/login")):
                self.__handle_connect(data[6:])
            elif(data.startswith("/ping")):
                self.__handle_ping(data[5:])
            elif(data.startswith("/success")):
                self.__handle_success(data[8:])
            elif(data.startswith("/failed")):
                self.__handle_failed(data[7:])
            elif(data.startswith("/disconnect")):
                self.__handle_disconnect(data[11:])
            else:
                self.__window.buffer_action("display;" + data)
        except Exception, err:
            if(not self.__connected):
                self.__window.buffer_action("notconnected;" + str(err))
                self.__quit()

    def writable(self):
        return len(self.__current_send) > 0 or (not self.__buffer.empty()) or (not self.__actions.empty())

    def handle_write(self):
        # handle actions first
        if(not self.__actions.empty()):
            self.__handle_actions()
            return

        # if no pending sends, get a new one
        while(self.writable()):
            if(len(self.__current_send) <= 0):
                self.__current_send = self.__buffer.get()

            sent = self.send(self.__current_send)
            self.__current_send = self.__current_send[sent:]

    def handle_close(self):
        self.__logger.warn("Server closed connection")
        self.__quit()

    def buffer_action(self, action):
        self.__actions.put(action)

    def buffer_send(self, command):
        self.__buffer.put(self.__message_generator.generate_message(command))

    def __disconnect(self):
        self.__logger.info("Disconnecting...")
        self.send(self.__message_generator.generate_message("/disconnect"))
        self.__quit()

    def __quit(self):
        self.__window.buffer_action("disconnected")
        self.close()

    def __handle_actions(self):
        while(not self.__actions.empty()):
            action = self.__actions.get()
            if(action == "quit"):
                self.__quit()
            elif(action == "disconnect"):
                self.__disconnect()
            elif(action.startswith("send")):
                self.buffer_send(action.split(";", 1)[1])
            else:
                self.__logger.warn("Invalid action: " + action)

    def __handle_connect(self, msg):
        self.__logger.info("Sending login info...")
        self.buffer_send("/login " + self.__user[0] + ";" + self.__user[1])

    def __handle_ping(self, msg):
        self.__logger.info("Sending ping response...")
        self.buffer_send("/ping")

    def __handle_success(self, msg):
        self.__connected = True
        self.__window.buffer_action("connected")

    def __handle_failed(self, msg):
        self.__connected = False
        self.__window.buffer_action("notconnected;Login failed")

    def __handle_disconnect(self, msg):
        self.__logger.info("Server disconnected")
        self.__quit()
