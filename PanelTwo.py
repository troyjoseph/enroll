import wx, thread
from checker import Nbr
import wx.lib.agw.shapedbutton as SB
from wx.lib.agw.shapedbutton import SButton, SBitmapButton






class PanelTwo(wx.Panel):
    """"""

    def __init__(self, parent):
        """Constructor"""
        self.semester = "SP15"
        wx.Panel.__init__(self, parent=parent)
        self.SetBackgroundColour('#3378BD')

        text = wx.StaticText(self, -1, "Enter classes")
        text.SetFont(wx.Font(33, wx.SWISS, wx.ITALIC,wx.BOLD))
        text.SetSize(text.GetBestSize())
        text.SetForegroundColour((253,253,253)) # set text color

        addLink1 = wx.StaticBitmap(self, -1, wx.Bitmap("add_smallx.png", wx.BITMAP_TYPE_ANY), (0, 0), (11, 11))
        addLink1.Bind(wx.EVT_LEFT_DOWN, self.onAddText1)
        removeLink1 = wx.StaticBitmap(self, -1, wx.Bitmap("remove_smallx.png", wx.BITMAP_TYPE_ANY), (0, 0), (11, 11))
        removeLink1.Bind(wx.EVT_LEFT_DOWN, self.onRemoveText1)

        addClassBtn = wx.Button(self, -1, "Add Class")
        self.text1 = 1
        self.text1a = wx.TextCtrl(self, -1, "Course nbr", size=(75, -1),  style = wx.TE_PROCESS_ENTER)
        self.txt1a = wx.StaticText(self, -1, "ABCD 1234")
        self.txt1a.SetForegroundColour((51,120,189)) 
        self.Bind(wx.EVT_TEXT_ENTER, self.onText1aChange, self.text1a)
        self.text1b = wx.TextCtrl(self, -1, "Linked nbr", size=(75, -1),  style = wx.TE_PROCESS_ENTER)
        self.txt1b = wx.StaticText(self, -1, "ABCD 1234")
        self.txt1b.SetForegroundColour((51,120,189))
        self.Bind(wx.EVT_TEXT_ENTER, self.onText1bChange, self.text1b)
        self.text1c = wx.TextCtrl(self, -1, "Linked nbr", size=(75, -1),  style = wx.TE_PROCESS_ENTER)
        self.txt1c = wx.StaticText(self, -1, "ABCD 1234")
        self.txt1c.SetForegroundColour((51,120,189))
        self.Bind(wx.EVT_TEXT_ENTER, self.onText1cChange, self.text1c)
        

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        text1s = wx.BoxSizer(wx.HORIZONTAL)
        txt1s = wx.BoxSizer(wx.HORIZONTAL)
        add1 = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(text, 0, wx.ALIGN_CENTER|wx.TOP, wx.TOP, 50)
        self.sizer.Add(addClassBtn, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        self.sizer.Add(text1s, 0, wx.ALIGN_CENTER|wx.TOP,20)
        self.sizer.Add(txt1s, 0, wx.ALIGN_CENTER|wx.ALIGN_LEFT, 172)
        text1s.Add(add1, 0, wx.ALIGN_CENTER|wx.RIGHT, 3)
        add1.Add(addLink1, 0, wx.ALIGN_CENTER|wx.TOP,0)
        add1.Add(removeLink1, 0, wx.ALIGN_CENTER|wx.TOP,0)
        text1s.Add(self.text1a, 0, wx.ALIGN_LEFT, 0)
        text1s.Add(self.text1b, 0, wx.ALIGN_CENTER, 0)
        text1s.Add(self.text1c, 0, wx.ALIGN_RIGHT, 0)
        txt1s.Add(self.txt1a, 0, wx.ALIGN_LEFT, 0)
        txt1s.Add(self.txt1b, 0, wx.ALIGN_CENTER, 0)
        txt1s.Add(self.txt1c, 0, wx.ALIGN_RIGHT, 0)

        self.text1b.Hide()
        self.text1c.Hide()
        self.SetSizer(self.sizer)
        self.Layout()

    def onText1aChange(self, event):
        thread.start_new_thread(self.changeText, (self.text1a,self.txt1a, ) )

    def onText1bChange(self, event):
        thread.start_new_thread(self.changeText, (self.text1b,self.txt1b, ) )

    def onText1cChange(self, event):
        thread.start_new_thread(self.changeText, (self.text1c,self.txt1c, ) )
            
    def onAddText1(self, event):
        if (self.text1 == 1):
            self.text1b.Show()
            self.txt1b.Show()
            self.SetSizer(self.sizer)
            self.Layout()
            self.text1 +=1
        elif (self.text1 == 2):
            self.text1c.Show()
            self.txt1c.Show()
            self.SetSizer(self.sizer)
            self.Layout()
            self.text1 +=1

    def onRemoveText1(self, event):
        if (self.text1 == 2):
            self.text1b.Hide()
            self.txt1b.Hide()
            self.SetSizer(self.sizer)
            self.Layout()
            self.text1 -=1
        elif (self.text1 == 3):
            self.text1c.Hide()
            self.txt1c.Hide()
            self.SetSizer(self.sizer)
            self.Layout()
            self.text1 -=1

    def changeText(self, text, txt):
        try:
            n = Nbr()
            nbr = n.get(self.semester, text.GetValue())
            print nbr
            txt.SetLabel(str(nbr))
            txt.SetForegroundColour((253,253,253)) 
        #textctrl is not an int    
        except Exception, e:
            print str(e)
            txt.SetLabel("")
