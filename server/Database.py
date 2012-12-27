class Database:
    """ Database subclass. """
    def __init__(self):
        pass

    def __del__(self):
        self.disconnect()

    def connect(self):
        return False

    def disconnect(self):
        pass

    def authenticate(self, username, password):
        return False

    def set_logged_in(self, username, loggedin):
        return False

    def get_logged_in(self, username):
        return False
