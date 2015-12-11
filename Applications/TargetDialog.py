# -*- coding: utf-8 -*-

__author__ = 'Jack'

import wx

class TargetDialog(wx.Dialog):
    def __init__(self, parent, id=-1, title=u'项目'):
        wx.Dialog.__init__(self, parent, id, title, size=(400, 250))
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.label1 = wx.StaticText(self, label=u'输入项目名称（英文）：')
        self.field1 = wx.TextCtrl(self, value=title, size=(300, 30))
        self.okbutton = wx.Button(self, label=u'确定', id=wx.ID_OK)
        self.cancelbutton = wx.Button(self, label=u'取消', id=wx.ID_CANCEL)

        self.mainSizer.Add(self.label1, 0, wx.ALL, 8)
        self.mainSizer.Add(self.field1, flag=wx.ALIGN_CENTER|wx.ALL, border=8)

        self.buttonSizer.Add(self.okbutton, 0, wx.ALL, 8)
        self.buttonSizer.Add(self.cancelbutton, 0, wx.ALL, 8)
        self.mainSizer.Add(self.buttonSizer, flag=wx.ALIGN_CENTER|wx.ALL, border=8)

        self.Bind(wx.EVT_BUTTON, self.OnOK, id=wx.ID_OK)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnOK)

        self.SetSizer(self.mainSizer)
        self.Centre()

        self.projectName = None

    def OnOK(self, e):
        if self.field1.GetValue() == '':
            wx.MessageBox('The project name should not be empty!', 'Error', wx.OK | wx.ICON_INFORMATION)
        else:
            self.projectName = self.field1.GetValue()
            self.Destroy()


