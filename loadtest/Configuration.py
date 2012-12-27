import logging
from ConfigParser import SafeConfigParser

class Configuration(SafeConfigParser):
    __configuration = None

    def __init__(self):
        # enforce singleton pattern
        if(not Configuration.__configuration == None):
            raise Configuration.__configuration
        Configuration.__configuration = self

        SafeConfigParser.__init__(self)

        # get a logger
        self.__logger = logging.getLogger("chattest.loadtest.Configuration")
        self.__logger.debug("Created a new Configuration object...")

        # create the default sections
        self.add_section("network")
        self.add_section("users")
        self.add_section("sleep")

        # set the default values
        self.set("network", "host", "localhost")
        self.set("network", "port", "8376")
        self.set("users", "amount", "50")
        self.set("users", "prefix", "loadtest")
        self.set("users", "password", "loadtest")
        self.set("sleep", "start", "5")
        self.set("sleep", "send", "1")

    def get_network_host(self):
        return self.get("network", "host")

    def get_network_port(self):
        return self.getint("network", "port")

    def get_users_amount(self):
        return self.getint("users", "amount")

    def get_users_prefix(self):
        return self.get("users", "prefix")

    def get_users_password(self):
        return self.get("users", "password")

    def get_sleep_start(self):
        return self.getint("sleep", "start")

    def get_sleep_send(self):
        return self.getint("sleep", "send")

    def dump(self):
        self.__logger.debug("Network Configuration:")
        self.__logger.debug("\thost = " + self.get_network_host())
        self.__logger.debug("\tport = %(port)d" % { "port": self.get_network_port() })

        self.__logger.debug("Users Configuration:")
        self.__logger.debug("\tamount = %(amount)d" % { "amount": self.get_users_amount() })
        self.__logger.debug("\tprefix = " + self.get_users_prefix())
        self.__logger.debug("\tpassword = " + self.get_users_password())

        self.__logger.debug("Sleep Configuration:")
        self.__logger.debug("\tstart = %(start)d" % { "start": self.get_sleep_start() })
        self.__logger.debug("\tsend = %(send)d" % { "send": self.get_sleep_send() })

# returns the global configuration
def configuration():
    try:
        configuration = Configuration()
    except Configuration, conf:
        configuration = conf
    return configuration
