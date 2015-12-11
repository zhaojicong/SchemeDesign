# -*- coding: utf-8 -*-

__author__ = 'Jack'

import wx

class ObjectiveDialog(wx.Dialog):
    def __init__(self, parent, id=-1, title=""):
        title.split(',')
        title = title.split(',')
        wx.Dialog.__init__(self, parent, id, title=u'目标 - '+title[0], size=[400, 500])
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        setting = [u'最大化', u'最小化']

        self.label1 = wx.StaticText(self, label=u'输入目标名称（英文）：')
        self.field1 = wx.TextCtrl(self, value=title[0], size=(300, 30))
        self.label2 = wx.StaticText(self, label=u'输入目标函数关系：')
        self.label3 = wx.StaticText(self, label=u'优化方向：')

        if title[1].startswith('-1*(') and title[1].endswith(')'):
            length = len(title[1])
            self.field2 = wx.TextCtrl(self, value=title[1][4:len(title[1])-1], size=(300, 100), style=wx.TE_MULTILINE)
            self.cb = wx.ComboBox(self, choices=setting, style=wx.CB_READONLY, size=(300, 40), value=u'最大化')
        else:
            self.field2 = wx.TextCtrl(self, value=title[1], size=(300, 100), style=wx.TE_MULTILINE)
            self.cb = wx.ComboBox(self, choices=setting, style=wx.CB_READONLY, size=(300, 40), value=u'最小化')
        self.okbutton = wx.Button(self, label=u'确定', id=wx.ID_OK)
        self.cancelbutton = wx.Button(self, label=u'取消', id=wx.ID_CANCEL)

        self.mainSizer.Add(self.label1, 0, wx.ALL, 8)
        self.mainSizer.Add(self.field1, flag=wx.ALIGN_CENTER|wx.ALL, border=8)
        self.mainSizer.Add(self.label2, 0, wx.ALL, 8)
        self.mainSizer.Add(self.field2, flag=wx.ALIGN_CENTER|wx.ALL, border=8)
        self.mainSizer.Add(self.label3, 0, wx.ALL, 8)
        self.mainSizer.Add(self.cb, flag=wx.ALIGN_CENTER|wx.ALL, border=8)
        self.buttonSizer.Add(self.okbutton, 0, wx.ALL, 8)
        self.buttonSizer.Add(self.cancelbutton, 0, wx.ALL, 8)
        self.mainSizer.Add(self.buttonSizer, flag=wx.ALIGN_CENTER|wx.ALL, border=8)

        self.Bind(wx.EVT_BUTTON, self.OnOK, id=wx.ID_OK)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnOK)

        self.SetSizer(self.mainSizer)
        self.Centre()
        self.objectiveName = None
        self.function = None

    def OnOK(self, e):
        if self.field1.GetValue() == '':
            wx.MessageBox('The objective name should not be empty!', 'Error', wx.OK | wx.ICON_INFORMATION)
        elif self.field2.GetValue() == '':
            wx.MessageBox('The function should not be empty!', 'Error', wx.OK | wx.ICON_INFORMATION)
        elif not self.cb.GetValue() == u'最大化' and not self.cb.GetValue() == u'最小化':
            wx.MessageBox('Please choose the objective direction', 'Error', wx.OK | wx.ICON_INFORMATION)
        else:
            self.objectiveName = self.field1.GetValue()
            if self.cb.GetValue() == u'最小化':
                self.function = self.field2.GetValue()
            else:
                self.function = '-1*('+self.field2.GetValue()+')'
            self.Destroy()


