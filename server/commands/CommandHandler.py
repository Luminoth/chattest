class CommandHandler:
    def __init__(self, command, client):
        # init member variables
        self.client = client
        self.command = command
        self.argument = None

    def owner(self, command):
        return command.startswith(self.command)

    def requires_login(self):
        raise NotImplementedError("CommandHandler.require_login is not implemented")

    def handle(self, command):
        self.argument = command[len(self.command) + 1:]
