import login, wx, thread
import wx


class MyFrame(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title, size=(700, 400)) 

        # Now create the Panel to put the other controls on.
        panel = wx.Panel(self)

        # and a few controls
        text = wx.StaticText(panel, -1, "Enroll Bot")
        text.SetFont(wx.Font(33, wx.SWISS, wx.NORMAL, wx.BOLD))
        text.SetSize(text.GetBestSize())
        text.SetForegroundColour((253,253,253)) # set text color
        self.netid = wx.TextCtrl(panel, -1, "NetID", size=(175, -1), style=wx.TE_RICH)
        self.password = wx.TextCtrl(panel, -1, "Password", size=(175, -1), style=wx.TE_PASSWORD)

        self.failtext = wx.StaticText(panel, -1, "The NetID or password you entered is incorrect.")
        self.failtext.SetForegroundColour((51,120,189))

        btn = wx.Button(panel, -1, "Login")

        # bind the button events to handlers
        self.Bind(wx.EVT_BUTTON, self.OnLogin, btn)
        # Use a sizer to layout the controls, stacked vertically and with
        # a 10 pixel border around each
        panel.SetBackgroundColour('#3378BD')
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(text, 0, wx.ALIGN_CENTER|wx.ALL, wx.TOP, 500)
        sizer.Add(self.netid, 0, wx.ALIGN_CENTER|wx.ALL, 0)
        sizer.Add(self.password, 0, wx.ALIGN_CENTER|wx.ALL, 0)
        sizer.Add(btn, 0, wx.ALIGN_CENTER|wx.ALL, 20)
        sizer.Add(self.failtext, 0, wx.ALIGN_CENTER|wx.ALL, 20)
        panel.SetSizer(sizer)
        panel.Layout()

        
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
        self.SetTopWindow(frame)
        frame.Show(True)
        return True
        
app = MyApp(redirect=True)
app.MainLoop()
