import login, wx, thread
from panelLogin import PanelLogin
from PanelTwo import PanelTwo
import wx.grid as gridlib 

 
########################################################################
class MyForm(wx.Frame):
 
    #----------------------------------------------------------------------
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title, size=(700, 400)) 
 
        self.panel_login = PanelLogin(self)
        self.panel_two = PanelTwo(self)
        self.panel_two.Hide()
 
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.panel_login, 1, wx.EXPAND)
        self.sizer.Add(self.panel_two, 1, wx.EXPAND)
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
        if self.panel_login.IsShown():
            self.SetTitle("Panel Two Showing")
            self.panel_login.Hide()
            self.panel_two.Show()
        else:
            self.SetTitle("Panel One Showing")
            self.panel_login.Show()
            self.panel_two.Hide()
        self.Layout()
    
    def tryLogin(self, netid, password):
        l = login.Helper()
        if (l.testLogin(netid, password) == False):
            self.failtext.SetLabel("The NetID or password you entered is incorrect.")
        else:
            self.panel_login.Hide()
            self.panel_two.Show()
            self.Layout()
            

    def OnLogin(self, evt):
        """Event handler for the button click."""

        self.failtext.SetLabel("Logging in....")
        self.failtext.SetForegroundColour((253,253,253))
        self.failtext.Refresh()
        thread.start_new_thread(self.tryLogin, (self.netid.GetValue(),self.password.GetValue(), ) )
 
# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyForm(None, "Enroll App")
    frame.Show()
    app.MainLoop()