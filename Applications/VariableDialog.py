# -*- coding: utf-8 -*-

__author__ = 'Jack'

import wx

class VariableDialog(wx.Dialog):
    def __init__(self, parent, id=-1, title=""):
        title.split(',')
        title = title.split(',')
        subject = u'变量 - '+'x'+title[0]
        wx.Dialog.__init__(self, parent, id, subject, size=[400, 400])
        self.initUI(title)
        self.variableName = None
        self.lowerBound = None
        self.upperBound = None

    def initUI(self, title):

        panel = wx.Panel(self)
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        rangeBox = wx.StaticBox(self, label=u'范围', size=(300,250))
        nameBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        rangeBoxSizer = wx.StaticBoxSizer(rangeBox, wx.VERTICAL)
        lowerSizer = wx.BoxSizer(wx.HORIZONTAL)
        upperSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        label1 = wx.StaticText(self, label=u'变量名：')
        self.field1 = wx.TextCtrl(self, value=title[1], size=(250, 30))  #Name of variable
        label21 = wx.StaticText(self, label=u'下边界（最小值）：')
        label22 = wx.StaticText(self, label=u'上边界（最大值）：')
        self.field21 = wx.TextCtrl(self, value=title[2], size=(120, 30))
        self.field22 = wx.TextCtrl(self, value=title[3], size=(120, 30))

        okbutton = wx.Button(self, label=u'确定', id=wx.ID_OK)
        cancelbutton = wx.Button(self, label=u'取消', id=wx.ID_CANCEL)

        lowerSizer.Add(label21, 0, wx.ALL, 8)
        lowerSizer.Add(self.field21, 0, wx.ALL, 8)
        upperSizer.Add(label22, 0, wx.ALL, 8)
        upperSizer.Add(self.field22, 0, wx.ALL, 8)
        rangeBoxSizer.Add(lowerSizer, 0, wx.ALL, 8)
        rangeBoxSizer.Add(upperSizer, 0, wx.ALL, 8)
        nameBoxSizer.Add(label1, 0, wx.ALL, 8)
        nameBoxSizer.Add(self.field1, 0, wx.ALL, 8)

        buttonSizer.Add(okbutton, 0, wx.ALL, 8)
        buttonSizer.Add(cancelbutton, 0, wx.ALL, 8)

        mainSizer.Add(nameBoxSizer, flag=wx.ALIGN_CENTER|wx.ALL, border=8)
        mainSizer.Add(rangeBoxSizer, flag=wx.ALIGN_CENTER|wx.ALL, border=8)
        mainSizer.Add(buttonSizer, flag=wx.ALIGN_CENTER|wx.ALL, border=8)

        self.Bind(wx.EVT_BUTTON, self.OnOK, id=wx.ID_OK)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnOK)

        self.SetSizer(mainSizer)
        self.Centre()

    def OnOK(self, e):
        lowerbound = self.field21.GetValue()
        upperbound = self.field22.GetValue()
        if self.field1.GetValue() == '':
            wx.MessageBox(u'变量名不能为空！', u'错误', wx.OK | wx.ICON_INFORMATION)
        elif not isfloat(lowerbound):
            wx.MessageBox(u'下边界数据类型应为浮点型！', u'错误', wx.OK | wx.ICON_INFORMATION)
        elif not isfloat(upperbound):
            wx.MessageBox(u'上边界数据类型应为浮点型！', u'错误', wx.OK | wx.ICON_INFORMATION)
        elif float(upperbound) <= float(lowerbound):
            wx.MessageBox(u'下边界应比上边界小！', u'错误', wx.OK | wx.ICON_INFORMATION)
        else:
            self.variableName = self.field1.GetValue()
            self.lowerBound = self.field21.GetValue()
            self.upperBound = self.field22.GetValue()
            self.Destroy()

def isfloat(number):
    try:
        float(number)
        return True
    except:
        return False

