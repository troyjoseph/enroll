import login, wx, thread
import wx

class PanelLogin(wx.Panel):

	def __init__(self, parent):
		wx.Panel.__init__(self, parent=parent)
		text = wx.StaticText(self, -1, "Enroll Bot")
        text.SetFont(wx.Font(33, wx.SWISS, wx.NORMAL, wx.BOLD))
        text.SetSize(text.GetBestSize())
        text.SetForegroundColour((253,253,253)) # set text color
        self.netid = wx.TextCtrl(self, -1, "NetID", size=(175, -1), style=wx.TE_RICH)
        self.password = wx.TextCtrl(self, -1, "Password", size=(175, -1), style=wx.TE_PASSWORD)
        self.failtext = wx.StaticText(self, -1, "The NetID or password you entered is incorrect.")
        self.failtext.SetForegroundColour((51,120,189))
        
        btn = wx.Button(panel, -1, "Login")
        self.Bind(wx.EVT_BUTTON, self.OnLogin, btn)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(text, 0, wx.ALIGN_CENTER|wx.ALL, wx.TOP, 500)
        sizer.Add(self.netid, 0, wx.ALIGN_CENTER|wx.ALL, 0)
        sizer.Add(self.password, 0, wx.ALIGN_CENTER|wx.ALL, 0)
        sizer.Add(btn, 0, wx.ALIGN_CENTER|wx.ALL, 20)
        sizer.Add(self.failtext, 0, wx.ALIGN_CENTER|wx.ALL, 20)

        self.SetSizer(sizer)

class MyFrame(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title, size=(700, 400)) 

        # Now create the Panel to put the other controls on.
        self.panel_login = PanelLogin(self)
        self.panel_login.SetBackgroundColour('#3378BD')
        self.panel_two = wx.Panel(self)
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.add(self.panel_login, 1, wx.EXPAND)
        self.sizer.add(self.panel_two, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        switch_panels_menu_item = fileMenu.Append(wx.ID_ANY, 
                                                  "Switch Panels", 
                                                  "Some text")
        self.Bind(wx.EVT_MENU, self.onSwitchPanels, 
                  switch_panels_menu_item)
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)
 
    #----------------------------------------------------------------------
    def onSwitchPanels(self, event):
        """"""
        if self.panel_one.IsShown():
            self.SetTitle("Panel Two Showing")
            self.panel_one.Hide()
            self.panel_two.Show()
        else:
            self.SetTitle("Panel One Showing")
            self.panel_one.Show()
            self.panel_two.Hide()
        self.Layout()

        
    def tryLogin(self, netid, password):
    	l = login.Helper()
    	if (l.testLogin(netid, password) == False):
        	self.failtext.SetLabel("The NetID or password you entered is incorrect.")
        else:
        	self.failtext.SetLabel("Success!")

    def OnLogin(self, evt):
        """Event handler for the button click."""

        self.failtext.SetLabel("Logging in....")
        self.failtext.SetForegroundColour((253,253,253))
        self.failtext.Refresh()
        thread.start_new_thread(self.tryLogin, (self.netid.GetValue(),self.password.GetValue(), ) )    	


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, "Enroll App")
        frame.Show(True)
        return True
        
app = MyApp(redirect=True)
app.MainLoop()
