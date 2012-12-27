import logging
from xml.sax import ContentHandler

class MessageParserError(Exception):
    """ Thrown when message parsing fails """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class MessageParser(ContentHandler):
    """ Parses the incoming XML stream.
        Available messages:
            message - A single message.
    """
    def __init__(self, handler):
        ContentHandler.__init__(self)

        # get a logger
        self.__logger = logging.getLogger("chattest.common.MessageParser")
        self.__logger.debug("Created a new MessageParser object...")

        # init member variables
        self.__handler = handler
        self.__state = []
        self.__message = ""

    def startElement(self, name, attrs):
        self.__logger.debug("<" + name + ">")

        # update the parser state
        if(name == "message"):
            self.__state.append(name)
        else:
            raise MessageParserError("Unknown start element: " + name)

    def endElement(self, name):
        # make sure the end element matches the start element
        if(len(self.__state) == 0 or (not self.__state_head() == name)):
            raise MessageParserError("Element mismatch: expected '" + self.__state_head() + "', got '" + name + "'")

        # pop the state and handle the element
        self.__logger.debug("</" + self.__state_head() + ">")
        self.__state.pop()
        if(name == "message"):
            self.__handler.handle_message(self.__message)
            self.__message = ""
        else:
            raise MessageParserError("Unknown end element: " + name)

    def characters(self, content):
        # we must be in an element here
        if(len(self.__state) == 0):
            raise MessageParserError("Characters found outside of element: " + content)

        # decide what to do based on the state
        if(self.__state_head() == "message"):
            self.__message = self.__message + content
        else:
            raise MessageParserError("Unknown message parser state: " + self.__state[0])

    def ignorableWhitespace(self, whitespace):
        # don't ignore whitespace in a message
        if(self.__state_head() == "message"):
            return False

        # ignore all other whitespace
        return True

    def skippedEntity(self, name):
        self.__logger.warn("Skipping entity: " + name)

    def __state_head(self):
        # TODO: there's gotta be a more Pythonish way to do this
        return self.__state[len(self.__state)-1]
