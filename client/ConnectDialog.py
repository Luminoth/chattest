import logging

from wxPython.wx import *
from wxPython.lib.intctrl import wxIntCtrl

from Configuration import configuration

class ConnectDialog(wxDialog):
    def __init__(self, parent):
        wxDialog.__init__(self, parent, -1, "Connect to...", size=(235, 110))

        # get a logger
        self.__logger = logging.getLogger("chattest.client.ConnectDialog")
        self.__logger.debug("Created a new ConnectDialog object...")

        # init member variables
        self.__configuration = configuration()

        # init controls
        self.__init_controls()

    def __init_controls(self):
        # host
        self.__host = wxTextCtrl(self, -1, self.__configuration.get_network_host())
        hbox = wxBoxSizer(wxHORIZONTAL)
        hbox.Add(self.__host, 1, wxEXPAND | wxALL, 1)

        # port
        self.__port = wxIntCtrl(self, -1, self.__configuration.get_network_port(), min=1, max=65536, limited=True)
        hbox.Add(self.__port, 0, wxEXPAND | wxALL, 1)

        grid = wxFlexGridSizer(3, 2, 2, 2)
        grid.Add(wxStaticText(self, -1, "Host:"), 0, wxALIGN_RIGHT | wxALL, 1)
        grid.Add(hbox)

        # username
        self.__username = wxTextCtrl(self, -1, self.__configuration.get_user_username())
        grid.Add(wxStaticText(self, -1, "Username:"), 0, wxALIGN_RIGHT | wxALL, 1)
        grid.Add(self.__username, 1, wxEXPAND | wxALL, 1)

        # password
        self.__password = wxTextCtrl(self, -1, style=wxTE_PASSWORD)
        grid.Add(wxStaticText(self, -1, "Password:"), 0, wxALIGN_RIGHT | wxALL, 1)
        grid.Add(self.__password, 1, wxEXPAND | wxALL, 1)

        topbox = wxBoxSizer(wxVERTICAL)
        topbox.Add(grid, flag=wxGROW)

        # button spacer
        hbox = wxBoxSizer(wxHORIZONTAL)
        hbox.Add(wxSize(1, 1), 1, wxEXPAND | wxALL, 1)

        # connect button
        button = wxButton(self, wxID_OK, "Connect")
        button.SetDefault()
        hbox.Add(button, 0, wxALL, 1)

        # cancel button
        button = wxButton(self, wxID_CANCEL, "Cancel")
        hbox.Add(button, 0, wxALL, 1)

        topbox.Add(hbox, 1, wxEXPAND)

        self.SetSizer(topbox)
        self.SetAutoLayout(True)
        topbox.Fit(self)

    def get_host(self):
        return self.__host.GetValue()

    def get_port(self):
        return self.__port.GetValue()

    def get_username(self):
        return self.__username.GetValue()

    def get_password(self):
        return self.__password.GetValue()
