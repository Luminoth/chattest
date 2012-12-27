from ConfigParser import SafeConfigParser

class Configuration(SafeConfigParser):
    __configuration = None

    def __init__(self):
        # enforce singleton pattern
        if(not Configuration.__configuration == None):
            raise Configuration.__configuration
        Configuration.__configuration = self

        SafeConfigParser.__init__(self)

        # create the default sections
        self.add_section("network")
        self.add_section("user")

        # set the default values
        self.set("network", "host", "localhost")
        self.set("network", "port", "8376")
        self.set("user", "username", "testuser")

    def get_network_host(self):
        return self.get("network", "host")

    def set_network_host(self, host):
        self.set("network", "host", host)

    def get_network_port(self):
        return self.getint("network", "port")

    def set_network_port(self, port):
        self.set("network", "port", str(port))

    def get_user_username(self):
        return self.get("user", "username")

    def set_user_username(self, username):
        self.set("user", "username", username)

# returns the global configuration
def configuration():
    try:
        configuration = Configuration()
    except Configuration, conf:
        configuration = conf
    return configuration
