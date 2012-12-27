import logging
import gc

from server.commands.CommandHandler import CommandHandler

class GarbageCollectionCommandHandler(CommandHandler):
    def __init__(self, client):
        CommandHandler.__init__(self, "/gc", client)

        # get a logger
        self.__logger = logging.getLogger("chattest.server.telnet.GarbageCollectionCommandHandler")
        self.__logger.debug("Created a new GarbageCollectionCommandHandler object...")

    def requires_login(self):
        return True

    def handle(self, command):
        CommandHandler.handle(self, command)

        if(self.argument == "collect"):
            self.client.buffer_send("Running garbage collector...\n")
            gc.collect()
        elif(self.argument == "enable"):
            if(gc.isenabled()):
                self.client.buffer_send("Garbage collector is already enabled!\n")
            else:
                self.client.buffer_send("Enabling garbage collector...\n")
                gc.enable()
        elif(self.argument == "disable"):
            if(not gc.isenabled()):
                self.client.buffer_send("Garbage collector is already disabled!\n")
            else:
                self.client.buffer_send("Disabling garbage collector...\n")
                gc.disable()
        else:
            self.client.buffer_send("Garbage Collector State\n")
            self.client.buffer_send("\tEnabled: " + str(gc.isenabled()) + "\n")
            self.client.buffer_send("\tObjects: %(objects)d\n" % { "objects": len(gc.get_objects()) })
            self.client.buffer_send("\tUncollectable %(garbage)d\n" % { "garbage": len(gc.garbage) })
