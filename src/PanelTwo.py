import wx
import thread
from checker import Nbr
import wx.lib.agw.shapedbutton as SB
from wx.lib.agw.shapedbutton import SButton, SBitmapButton
from bot import Bot
from preferences import Preferences


class PanelTwo(wx.Panel):

    def better_bind(self, type, instance, handler, *args, **kwargs):
        self.Bind(
            type, lambda event: handler(event, *args, **kwargs), instance)

    def __init__(self, parent):
        self.MAXCLASSES = Preferences.MAXCLASSES
        self.MAXLINKEDCLASSES = Preferences.MAXLINKEDCLASSES
        self.semester = Preferences.semester

        wx.Panel.__init__(self, parent=parent)
        self.SetBackgroundColour('#3378BD')

        text = wx.StaticText(self, -1, "Enroll Bot")
        text.SetFont(wx.Font(33, wx.SWISS, wx.NORMAL, wx.BOLD))
        text.SetSize(text.GetBestSize())
        text.SetForegroundColour((253, 253, 253))  # set text color

        self.addLinkedBtn = [0 for x in range(self.MAXCLASSES)]
        self.removeLinkedBtn = [0 for x in range(self.MAXCLASSES)]

        for r in range(0, self.MAXCLASSES):
            self.addLinkedBtn[r] = wx.StaticBitmap(
                self, -1, wx.Bitmap("src/images/add.png", wx.BITMAP_TYPE_ANY), (0, 0), (11, 11))
            self.addLinkedBtn[r].Bind(wx.EVT_LEFT_DOWN,  self.onAddTxt)
            self.removeLinkedBtn[r] = wx.StaticBitmap(
                self, -1, wx.Bitmap("src/images/remove.png", wx.BITMAP_TYPE_ANY), (0, 0), (11, 11))
            self.removeLinkedBtn[r].Bind(wx.EVT_LEFT_DOWN, self.onRemoveTxt)

        # goBtn = wx.StaticBitmap(self, -1, wx.Bitmap("go_small.png", wx.BITMAP_TYPE_ANY), (0, 0), (50, 50))
        # self.goBtn.Bind(wx.EVT_LEFT_DOWN,  self.onGo)
        bmp = wx.Bitmap("src/images/go.png", wx.BITMAP_TYPE_ANY)
        self.goBtn = SBitmapButton(self, wx.ID_ANY, bitmap=bmp)
        self.goBtn.Bind(wx.EVT_BUTTON, lambda event: self.onGo(event, parent))

        self.classes = 0
        addClassBtn = wx.Button(self, -1, "Add Class")
        removeClassBtn = wx.Button(self, -1, "Remove Class")
        addClassBtn.Bind(wx.EVT_BUTTON,  self.onAddClass)
        removeClassBtn.Bind(wx.EVT_BUTTON,  self.onRemoveClass)

        self.textCounter = [1 for x in range(self.MAXCLASSES)]
        self.text = [
            [0 for x in range(self.MAXLINKEDCLASSES)] for x in range(self.MAXCLASSES)]
        self.txt = [
            [0 for x in range(self.MAXLINKEDCLASSES)] for x in range(self.MAXCLASSES)]

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(text, 0, wx.ALIGN_CENTER | wx.TOP, wx.TOP, 50)
        addRemoveSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(addRemoveSizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        addRemoveSizer.Add(addClassBtn, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        addRemoveSizer.Add(removeClassBtn, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        textSizer = [0 for x in range(self.MAXCLASSES)]
        txtSizer = [0 for x in range(self.MAXCLASSES)]
        addSizer = [0 for x in range(self.MAXCLASSES)]
        for r in range(0, self.MAXCLASSES):
            textSizer[r] = wx.BoxSizer(wx.HORIZONTAL)
            txtSizer[r] = wx.BoxSizer(wx.HORIZONTAL)
            addSizer[r] = wx.BoxSizer(wx.VERTICAL)
            self.sizer.Add(textSizer[r], 0, wx.ALIGN_CENTER | wx.TOP, 2)
            self.sizer.Add(
                txtSizer[r], 0, wx.ALIGN_CENTER | wx.ALIGN_LEFT, 172)
            textSizer[r].Add(addSizer[r], 0, wx.ALIGN_CENTER | wx.RIGHT, 3)
            addSizer[r].Add(
                self.addLinkedBtn[r], 0, wx.ALIGN_CENTER | wx.TOP, 0)
            addSizer[r].Add(
                self.removeLinkedBtn[r], 0, wx.ALIGN_CENTER | wx.TOP, 0)

        self.sizer.Add(self.goBtn, 0, wx.ALIGN_CENTER | wx.TOP, 10)

        for r in range(0, self.MAXCLASSES):
            for c in range(0, self.MAXLINKEDCLASSES):
                self.text[r][c] = wx.TextCtrl(
                    self, -1, "Course nbr", size=(75, -1),  style=wx.TE_PROCESS_ENTER)
                self.txt[r][c] = wx.StaticText(self, -1, "ABCD 1234")
                self.txt[r][c].SetForegroundColour((51, 120, 189))
                self.better_bind(
                    wx.EVT_TEXT_ENTER, self.text[r][c], self.onTextChange, r, c)
                textSizer[r].Add(
                    self.text[r][c], 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 3)
                txtSizer[r].Add(self.txt[r][c], 0, wx.ALIGN_CENTER, 0)
                self.text[r][c].Hide()
                self.txt[r][c].Hide()
                self.addLinkedBtn[r].Hide()
                self.removeLinkedBtn[r].Hide()

        self.addLinkedBtn[0].Show()
        self.removeLinkedBtn[0].Show()
        self.text[0][0].Show()
        self.txt[0][0].Show()
        self.SetSizer(self.sizer)
        self.Layout()

    def onTextChange(self, event, r, c):
        thread.start_new_thread(
            self.changeText, (self.text[r][c], self.txt[r][c], ))

    def changeText(self, text, txt):
        try:
            n = Nbr()
            nbr = n.get(self.semester, text.GetValue())
            txt.SetLabel(str(nbr))
            txt.SetForegroundColour((253, 253, 253))
        # textctrl is not an int
        except Exception, e:
            print str(e)
            txt.SetLabel("")

    def onAddTxt(self, event):
        r = (int(event.GetId()) + 2015) * (-1) / 2
        if (self.textCounter[r] == 1):
            self.text[r][1].SetLabel("Discuss nbr")
            self.text[r][1].Show()
            self.txt[r][1].Show()
            self.SetSizer(self.sizer)
            self.Layout()
            self.textCounter[r] += 1
        elif (self.textCounter[r] == 2):
            self.text[r][2].SetLabel("Lab nbr")
            self.text[r][2].Show()
            self.txt[r][2].Show()
            self.SetSizer(self.sizer)
            self.Layout()
            self.textCounter[r] += 1

    def onRemoveTxt(self, event):
        r = (int(event.GetId()) + 2016) * (-1) / 2
        if (self.textCounter[r] == 2):
            self.text[r][1].Hide()
            self.txt[r][1].Hide()
            self.SetSizer(self.sizer)
            self.Layout()
            self.textCounter[r] -= 1
        elif (self.textCounter[r] == 3):
            self.text[r][2].Hide()
            self.txt[r][2].Hide()
            self.SetSizer(self.sizer)
            self.Layout()
            self.textCounter[r] -= 1

    def onAddClass(self, event):
        if (self.classes < self.MAXCLASSES - 1):
            self.classes += 1
            self.text[self.classes][0].Show()
            self.txt[self.classes][0].Show()
            self.addLinkedBtn[self.classes].Show()
            self.removeLinkedBtn[self.classes].Show()
            self.Layout()

    def onRemoveClass(self, event):
        if (self.classes > 0):
            for c in range(self.MAXLINKEDCLASSES):
                self.text[self.classes][c].SetLabel("Course nbr")
                self.text[self.classes][c].Hide()
                self.txt[self.classes][c].Hide()
            self.addLinkedBtn[self.classes].Hide()
            self.removeLinkedBtn[self.classes].Hide()
            self.classes -= 1
            self.Layout()

    def onGo(self, event, parent):

        bots = [Bot() for x in range(self.MAXCLASSES)]
        for r in range(0, self.MAXCLASSES):  # self.MAXCLASSES)
            # try:
            # there is something in this row
            if (str(self.text[r][0].GetValue()) != "Course nbr"):
                print 'start'
                thread.start_new_thread(bots[r].addClass, (parent.netid.GetValue(), parent.password.GetValue(), str(
                    self.text[r][0].GetValue()), str(self.text[r][1].GetValue()), str(self.text[r][2].GetValue()),))
            # except:
            #    print 'failed to add class, please contiune manually'
