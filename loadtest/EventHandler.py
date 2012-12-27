import errno
import logging
import asyncore
import socket
import time
from xml.sax import SAXException, make_parser
from Queue import Queue

from common.MessageGenerator import MessageGenerator
from common.MessageParser import MessageParser, MessageParserError

from Configuration import configuration
from MessageHandler import MessageHandler

class EventHandler(asyncore.dispatcher):
    def __init__(self, id):
        asyncore.dispatcher.__init__(self)

        # get a logger
        self.__logger = logging.getLogger("chattest.loadtest.EventHandler")
        self.__logger.debug("Created a new EventHandler object...")

        # get a configuration
        self.__configuration = configuration()

        # init member variables
        self.__server = (self.__configuration.get_network_host(), self.__configuration.get_network_port())
        self.__user = (self.__configuration.get_users_prefix() + str(id), self.__configuration.get_users_password())
        self.__message_generator = MessageGenerator()
        self.__message_parser = make_parser()
        self.__message_parser.setContentHandler(MessageParser(MessageHandler(self)))
        self.__attempted_connect = False
        self.__connected = False
        self.__buffer = Queue()
        self.__current_send = ""

        # create the socket
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)

    def handle_connect(self):
        self.__logger.warn(self.__user[0] + ": handle_connect")

    def handle_expt(self):
        self.__logger.warn(self.__user[0] + ": handle_expt")
        self.quit()

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

                self.__logger.warn(self.__user[0] + ": read error - " + str(err))
                self.quit()
                break
            except Exception, err:
                if(not self.__connected):
                    self.__logger.warn(self.__user[0] + ": error - " + str(err))
                    self.quit()
                break

    def writable(self):
        # connect to the server if we haven't already
        if(not self.__attempted_connect):
            self.__logger.info(self.__user[0] + ": connecting to %(host)s:%(port)d as '%(name)s'..." % { "host": self.__server[0], "port": self.__server[1], "name": self.__user[0] })
            self.connect(self.__server)
            self.__attempted_connect = True

        return len(self.__current_send) > 0 or (not self.__buffer.empty())

    def handle_write(self):
        # if no pending sends, get a new one
        while(self.writable()):
            if(len(self.__current_send) <= 0):
                self.__current_send = self.__buffer.get()

            # send the command
            sent = self.send(self.__current_send)
            self.__current_send = self.__current_send[sent:]

        # cool off to avoid overlapping sends
        time.sleep(self.__configuration.get_sleep_send())

    def handle_close(self):
        self.__logger.warn(self.__user[0] + ": server closed connection")
        self.quit()

    def buffer_send(self, command):
        self.__logger.debug(self.__user[0] + ": sending '" + command + "'")
        self.__buffer.put(self.__message_generator.generate_message(command))

    def disconnect(self):
        self.__logger.info(self.__user[0] + ": disconnecting...")
        self.send(self.__message_generator.generate_message("/disconnect"))
        self.quit()

    def quit(self):
        self.__logger.info(self.__user[0] + ": event handler quiting...")
        self.close()

    def handle_command(self, command):
        if(command.startswith("/login")):
            self.__handle_connect(command[6:])
        elif(command.startswith("/ping")):
            self.__handle_ping(command[5:])
        elif(command.startswith("/success")):
            self.__handle_success(command[8:])
        elif(command.startswith("/failed")):
            self.__handle_failed(command[7:])
        elif(command.startswith("/disconnect")):
            self.__handle_disconnect(command[11:])
        else:
            self.__logger.info("server: " + command)

    def __handle_connect(self, msg):
        self.__logger.info(self.__user[0] + ": sending login info...")
        self.buffer_send("/login " + self.__user[0] + ";" + self.__user[1])

    def __handle_ping(self, msg):
        self.__logger.info(self.__user[0] + ": sending ping response...")
        self.buffer_send("/ping")

    def __handle_success(self, msg):
        self.__logger.info(self.__user[0] + ": login successful")
        self.__connected = True

    def __handle_failed(self, msg):
        self.__logger.info(self.__user[0] + ": login failed")
        self.__connected = False

    def __handle_disconnect(self, msg):
        self.__logger.info(self.__user[0] + ": server disconnected")
        self.quit()
