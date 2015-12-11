# -*- coding: utf-8 -*-

__author__ = 'Jack'

import wx
from wxmplot import PlotApp

class ChartDialog(wx.Dialog):
    def __init__(self, parent, id=-1, title=""):
        self.result = title.__getitem__('result')
        self.objectivenames = title.__getitem__('objectivenames')
        self.objectivenumber = len(self.objectivenames)
        self.variablenames = title.__getitem__('variablenames')
        self.variablenumber = len(self.variablenames)
        wx.Dialog.__init__(self, parent, id, title=u'结果', size=(400, 350),
                           style=wx.DEFAULT_DIALOG_STYLE|wx.THICK_FRAME|wx.RESIZE_BORDER|wx.TAB_TRAVERSAL)
        self.xcb = wx.ComboBox(self, choices=self.objectivenames, style=wx.CB_READONLY)
        self.ycb = wx.ComboBox(self, choices=self.objectivenames, style=wx.CB_READONLY)
        drawButton = wx.Button(self, label=u'确定', id=wx.ID_ANY)
        quitButton = wx.Button(self, label=u'退出', id=wx.ID_CANCEL)
        xlabel = wx.StaticText(self, label=u'横坐标（x）：')
        ylabel = wx.StaticText(self, label=u'纵坐标（y）：')
        xBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        yBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        xBoxSizer.Add(xlabel, 0, wx.ALL, 8)
        xBoxSizer.Add(self.xcb, 0, wx.ALL, 8)
        yBoxSizer.Add(ylabel, 0, wx.ALL, 8)
        yBoxSizer.Add(self.ycb, 0, wx.ALL, 8)
        buttonSizer.Add(drawButton, 0, wx.ALL, 8)
        buttonSizer.Add(quitButton, 0, wx.ALL, 8)
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        MainSizer.Add(xBoxSizer, 0, wx.ALL, 8)
        MainSizer.Add(yBoxSizer, 0, wx.ALL, 8)
        MainSizer.Add(buttonSizer, 0,wx.ALL, 8)
        self.SetSizer(MainSizer)

        self.Bind(wx.EVT_BUTTON, self.drawAPP, drawButton)

    def drawAPP(self, e):
        self.app = PlotApp()
        try:
            xlabel = self.xcb.GetValue()
            xindex = self.objectivenames.index(xlabel)
            ylabel = self.ycb.GetValue()
            yindex = self.objectivenames.index(ylabel)
        except:
            wx.MessageBox(u'请先选择x，y数据', u'提示', wx.OK | wx.ICON_INFORMATION)
        x = []
        y = []
        for individual in self.result:
            x.append(individual[xindex])
            y.append(individual[yindex])

        self.app.plot(x, y, title=xlabel+' - '+ylabel, label=xlabel+' - '+ylabel, xlabel=xlabel, ylabel=ylabel)
        self.app.run()
