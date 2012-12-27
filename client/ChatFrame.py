import logging
from Queue import Queue

from wxPython.wx import *

from Configuration import configuration
from ConnectDialog import ConnectDialog
from CommunicationThread import CommunicationThread

ID_CONNECT    = 101
ID_DISCONNECT = 102
ID_EXIT       = 103
ID_ABOUT      = 104
ID_SEND       = 201

class ChatFrame(wxFrame):
    def __init__(self, parent, id, title, size):
        wxFrame.__init__(self, parent, id, title, size=size)

        # get a logger
        self.__logger = logging.getLogger("chattest.client.ChatFrame")
        self.__logger.debug("Created a new ChatFrame object...")

        # init member variables
        self.__configuration = configuration()
        self.__actions = Queue()
        self.__thread = None

        # init timer
        self.__timer = wxPyTimer(self.__process_actions)
        self.__timer.Start(500)

        # init controls
        self.__init_statusbar()
        self.__init_menu()
        self.__init_controls()

        # init events
        EVT_CLOSE(self, self.OnClose)

    def __init_statusbar(self):
        self.CreateStatusBar()
        self.SetStatusText("Okay")

    def __init_menu(self):
        menuBar = wxMenuBar()
        self.__init_file_menu(menuBar)
        self.__init_help_menu(menuBar)

        self.SetMenuBar(menuBar)

    def __init_file_menu(self, menuBar):
        menu = wxMenu()

        menu.Append(ID_CONNECT, "&Connect...", "Connect to a server")
        EVT_MENU(self, ID_CONNECT, self.OnConnect)

        item = menu.Append(ID_DISCONNECT, "&Disconnect...", "Disconnect from the server")
        item.Enable(False)
        EVT_MENU(self, ID_DISCONNECT, self.OnDisconnect)

        menu.Append(ID_EXIT, "E&xit", "Terminate the program")
        EVT_MENU(self, ID_EXIT,  self.OnExit)

        menuBar.Append(menu, "&File")

    def __init_help_menu(self, menuBar):
        menu = wxMenu()

        menu.Append(ID_ABOUT, "&About", "More information about this program")
        EVT_MENU(self, ID_ABOUT, self.OnAbout)

        menuBar.Append(menu, "&Help")

    def __init_controls(self):
        # output
        self.__output = wxTextCtrl(self, -1, style=wxTE_MULTILINE | wxTE_PROCESS_TAB | wxTE_READONLY | wxTE_RICH2 | wxTE_AUTO_URL)
        hbox = wxBoxSizer(wxHORIZONTAL)
        hbox.Add(self.__output, 1, wxEXPAND | wxALL, 1)

        # user list
        self.__userlist = wxListCtrl(self, -1, style=wxLC_LIST)
        hbox.Add(self.__userlist, 0, wxEXPAND | wxALL, 1)

        topbox = wxBoxSizer(wxVERTICAL)
        topbox.Add(hbox, 1, wxEXPAND)

        # input
        self.__input = wxTextCtrl(self, -1)
        hbox = wxBoxSizer(wxHORIZONTAL)
        hbox.Add(self.__input, 1, wxEXPAND | wxALL, 1)

        # send button
        button = wxButton(self, ID_SEND, "Send")
        button.SetDefault()
        hbox.Add(button, 0, wxALL, 1)
        EVT_BUTTON(self, ID_SEND, self.OnSend)

        topbox.Add(hbox, 0, wxEXPAND)

        self.SetSizer(topbox)
        self.SetAutoLayout(True)
        topbox.Fit(self)

    def OnClose(self, event):
        self.__disconnect()
        self.Destroy()

    def OnConnect(self, event):
        dlg = ConnectDialog(self)
        ret = dlg.ShowModal()
        dlg.Destroy()

        if(ret == wxID_OK):
            self.__configuration.set_network_host(dlg.get_host())
            self.__configuration.set_network_port(dlg.get_port())
            self.__configuration.set_user_username(dlg.get_username())

            self.__connect((dlg.get_host(), dlg.get_port()), (dlg.get_username(), dlg.get_password()))

    def OnDisconnect(self, event):
        self.__disconnect()

    def OnExit(self, event):
        self.Close(True)

    def OnAbout(self, event):
        dlg = wxMessageDialog(self, "Nothing here yet", "About Client", wxOK | wxICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def OnSend(self, event):
        if(self.__thread == None):
            self.__logger.warn("Not connected")
            return

        text = self.__input.GetValue()
        if(len(text) <= 0):
            self.__logger.warn("Can't send empty value")
            return

        self.__logger.info("Sending: " + text)
        self.__thread.buffer_action("send;" + text)
        self.__input.Clear()

    def buffer_action(self, action):
        self.__actions.put(action)

    def __process_actions(self):
        while(not self.__actions.empty()):
            action = self.__actions.get()
            if(action.startswith("notconnected")):
                msg = action.split(";", 1)[1]
                self.__connect_update(False, msg)
            elif(action == "disconnected"):
                self.__disconnected()
            elif(action == "connected"):
                self.__connect_update(True)
            elif(action.startswith("display")):
                text = action.split(";", 1)[1]
                self.__logger.info("Displaying '" + text + "'")
                self.__output.AppendText(text)
            else:
                self.__logger.warn("Unknown action '" + action + "'")

    def __connect_update(self, success, msg=None):
        self.GetMenuBar().FindItemById(ID_CONNECT).Enable(not success)
        self.GetMenuBar().FindItemById(ID_DISCONNECT).Enable(success)

        if(success):
            self.SetStatusText("Connected")
        else:
            self.SetStatusText("Connection Failed")

            dlg = wxMessageDialog(self, "Connection failed: " + msg, "Connection Failed", wxOK | wxICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()

    def __disconnected(self):
        self.GetMenuBar().FindItemById(ID_CONNECT).Enable(True)
        self.GetMenuBar().FindItemById(ID_DISCONNECT).Enable(False)

        self.SetStatusText("Disconnected")

        self.__thread = None

    def __connect(self, server, user):
        self.GetMenuBar().FindItemById(ID_CONNECT).Enable(False)
        self.GetMenuBar().FindItemById(ID_DISCONNECT).Enable(False)

        self.SetStatusText("Connecting")

        self.__thread = CommunicationThread(server, user, self)
        self.__thread.start()

    def __disconnect(self):
        if(self.__thread):
            self.GetMenuBar().FindItemById(ID_CONNECT).Enable(False)
            self.GetMenuBar().FindItemById(ID_DISCONNECT).Enable(False)

            self.SetStatusText("Disconnecting")
            self.__thread.buffer_action("disconnect")
            self.__thread.join()
        else:
            self.__logger.debug("No thread to disconnect")
            self.__disconnected()
