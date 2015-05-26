import wx

class PanelLogin(wx.Panel):
 
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        self.SetBackgroundColour('#3378BD')
        self.clicked = False
        parent.text = wx.StaticText(self, -1, "Enroll Bot")
        textDontWant = wx.StaticText (self,-1, "Don't want to give us your password?")
        textDontWant.Bind(wx.EVT_LEFT_DOWN, lambda event: self.onClick(event, parent)) 
        font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        font.SetUnderlined(True)
        textDontWant.SetFont(font)
        parent.text.SetFont(wx.Font(33, wx.SWISS, wx.NORMAL, wx.BOLD))
        parent.text.SetSize(parent.text.GetBestSize())
        parent.text.SetForegroundColour((253,253,253)) # set text color

        parent.netid = wx.TextCtrl(self, -1, "NetID", size=(175, -1), style=wx.TE_RICH)
        parent.netid.SetForegroundColour((100,100,100))
        parent.netid.Bind(wx.EVT_SET_FOCUS, lambda event: self.onClick(event, parent)) 
        parent.password = wx.TextCtrl(self, -1, "Password", size=(175, -1), style=wx.TE_PASSWORD)
        parent.password.SetForegroundColour((100,100,100))
        parent.password.Bind(wx.EVT_SET_FOCUS, lambda event: self.onClick(event, parent)) 

        parent.failtext = wx.StaticText(self, -1, "The NetID or password you entered is incorrect.")
        parent.failtext.SetForegroundColour((51,120,189))
        parent.btn = wx.Button(self, -1, "Login")
        
        parent.Bind(wx.EVT_BUTTON, parent.OnLogin, parent.btn)
        parent.password.Bind(wx.EVT_TEXT_ENTER, parent.OnLogin)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(parent.text, 0, wx.ALIGN_CENTER|wx.ALL, wx.TOP, 500)
        sizer.Add(parent.netid, 0, wx.ALIGN_CENTER|wx.ALL, 0)
        sizer.Add(parent.password, 0, wx.ALIGN_CENTER|wx.ALL, 0)
        sizer.Add(parent.btn, 0, wx.ALIGN_CENTER|wx.ALL, 20)
        sizer.Add(parent.failtext, 0, wx.ALIGN_CENTER|wx.ALL, 20)
        sizer.Add(textDontWant, 0, wx.ALIGN_CENTER|wx.ALL, 20)
        self.SetSizer(sizer)
        self.Layout()


    def onClick(self, event, parent):
        if (event.GetId()==-2010):
            parent.netid.ChangeValue("")
            parent.netid.SetForegroundColour((0,0,0))
            self.Layout()
        if (event.GetId()==-2011):
            if (self.clicked == False):
                parent.password.ChangeValue("")
                parent.password.SetForegroundColour((0,0,0))
                self.Layout()
                self.clicked = True

        if (event.GetId()==-2009):
            dlg = wx.MessageDialog(None, 'If you would prefer to not share your password, you can log in manually to each window.', '', wx.OK | wx.CANCEL)
            result = dlg.ShowModal()
            if result == wx.ID_OK:
                parent.password.ChangeValue("")
                parent.panel_two.Show()
                self.Hide()
                parent.Layout()
                dlg.Destroy()
