import logging
from ConfigParser import SafeConfigParser

class ConfigurationError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
         return repr(self.value)

class Configuration(SafeConfigParser):
    __configuration = None

    def __init__(self):
        # enforce singleton pattern
        if(not Configuration.__configuration == None):
            raise Configuration.__configuration
        Configuration.__configuration = self

        SafeConfigParser.__init__(self)

        # get a logger
        self.__logger = logging.getLogger("chattest.server.Configuration")
        self.__logger.debug("Created a new Configuration object...")

        # create the default sections
        self.add_section("network")
        self.add_section("database")
        self.add_section("miscellaneous")
        self.add_section("telnet")

        # set the default values
        self.set("miscellaneous", "daemon", "true")
        self.set("miscellaneous", "ping", "1")
        self.set("miscellaneous", "timeout", "5")
        self.set("network", "port", "8376")
        self.set("database", "type", "local")
        self.set("database", "host", "localhost")
        self.set("database", "database", "chattest")
        self.set("database", "user", "root")
        self.set("database", "password", "password")
        self.set("telnet", "port", "8377")
        self.set("telnet", "user", "telnet")
        self.set("telnet", "password", "telnet")

    def validate(self):
        if(self.get_misc_timeout() <= self.get_misc_ping()):
            raise ConfigurationError("Timeout must be greater than ping")

    def get_misc_daemon(self):
        return self.getboolean("miscellaneous", "daemon")

    def get_misc_ping(self):
        return self.getint("miscellaneous", "ping")

    def get_misc_timeout(self):
        return self.getint("miscellaneous", "timeout")

    def get_network_port(self):
        return self.getint("network", "port")

    def get_database_type(self):
        return self.get("database", "type")

    def get_database_host(self):
        return self.get("database", "host")

    def get_database_database(self):
        return self.get("database", "database")

    def get_database_user(self):
        return self.get("database", "user")

    def get_database_password(self):
        return self.get("database", "password")

    def get_telnet_port(self):
        return self.getint("telnet", "port")

    def get_telnet_user(self):
        return self.get("telnet", "user")

    def get_telnet_password(self):
        return self.get("telnet", "password")

    def dump(self):
        self.__logger.debug("Miscellaneous Configuration:")
        self.__logger.debug("\tdaemon = " + str(self.get_misc_daemon()))
        self.__logger.debug("\tping = %(ping)d" % { "ping": self.get_misc_ping() })
        self.__logger.debug("\ttimeout = %(timeout)d" % { "timeout": self.get_misc_timeout() })

        self.__logger.debug("Network Configuration:")
        self.__logger.debug("\tport = %(port)d" % { "port": self.get_network_port() })

        self.__logger.debug("Database Configuration:")
        self.__logger.debug("\ttype = " + self.get_database_type())
        self.__logger.debug("\thost = " + self.get_database_host())
        self.__logger.debug("\tdatabase = " + self.get_database_database())
        self.__logger.debug("\tuser = " + self.get_database_user())
        self.__logger.debug("\tpassword = " + self.get_database_password())

        self.__logger.debug("Telnet Configuration:")
        self.__logger.debug("\tport = %(port)d" % { "port": self.get_telnet_port() })
        self.__logger.debug("\tuser = " + self.get_telnet_user())
        self.__logger.debug("\tpassword = " + self.get_telnet_password())

# returns the global configuration
def configuration():
    try:
        configuration = Configuration()
    except Configuration, conf:
        configuration = conf
    return configuration
