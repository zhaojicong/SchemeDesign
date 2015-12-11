# -*- coding: utf-8 -*-

__author__ = 'Jack'
import wx

class NewDialog(wx.Dialog):
    def __init__(self, parent, id=-1, title=u'新建项目'):
        wx.Dialog.__init__(self, parent, id, title, size=[400,500])
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.dirSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.label1 = wx.StaticText(self, label=u'项目名称')
        self.field1 = wx.TextCtrl(self, value="Untitled", size=(300, 30))
        self.label2 = wx.StaticText(self, label=u'目标个数')
        self.field2 = wx.TextCtrl(self, value="3", size=(300, 30))
        self.label3 = wx.StaticText(self, label=u'变量个数')
        self.field3 = wx.TextCtrl(self, value="4", size=(300, 30))
        self.okbutton = wx.Button(self, label=u'确定', id=wx.ID_OK)
        self.cancelbutton = wx.Button(self, label=u'取消', id=wx.ID_CANCEL)
        self.label4 = wx.StaticText(self, label=u'文件位置')
        self.field4 = wx.TextCtrl(self, size=(200, 30), value='C:\\Users\\Jack\\Desktop')
        self.browsebutton = wx.Button(self, label=u'浏览', id=wx.ID_ANY, size=(100, 30))

        self.mainSizer.Add(self.label1, 0, wx.ALL, 8)
        self.mainSizer.Add(self.field1, flag=wx.ALIGN_CENTER, border=8)
        self.mainSizer.Add(self.label2, 0, wx.ALL, 8)
        self.mainSizer.Add(self.field2, flag=wx.ALIGN_CENTER, border=8)
        self.mainSizer.Add(self.label3, 0, wx.ALL, 8)
        self.mainSizer.Add(self.field3, flag=wx.ALIGN_CENTER, border=8)
        self.mainSizer.Add(self.label4, 0, wx.ALL, 8)

        self.dirSizer.Add(self.field4, 0, wx.ALL, 0)
        self.dirSizer.Add(self.browsebutton, 0, wx.ALL, 0)
        self.mainSizer.Add(self.dirSizer, flag=wx.ALIGN_CENTER|wx.ALL, border=10)

        self.buttonSizer.Add(self.okbutton, 0, wx.ALL, 8)
        self.buttonSizer.Add(self.cancelbutton, 0, wx.ALL, 8)
        self.mainSizer.Add(self.buttonSizer, flag=wx.ALIGN_CENTER|wx.ALL, border=20)

        self.Bind(wx.EVT_BUTTON, self.OnOK, id=wx.ID_OK)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnOK)
        self.browsebutton.Bind(wx.EVT_BUTTON, self.OnBrowse)

        self.SetSizer(self.mainSizer)
        self.Centre()

        self.projectName = None
        self.objectiveNumber = 0
        self.variableNumber = 0
        self.dirPath = None

    def OnBrowse(self, e):
        dlg = wx.DirDialog (None, u'选择保存路径', 'C:\\Users\\Jack\\Desktop',
                            wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_CANCEL:
            return
        self.field4.SetValue(dlg.GetPath())

        dlg.Destroy()

    def OnOK(self, e):
        if self.field1.GetValue() == '':
            wx.MessageBox(u'项目名称不能为空!', u'错误', wx.OK | wx.ICON_ERROR)
        elif not is_qualified(self.field2.GetValue()):
            wx.MessageBox(u'目标个数必须为1~9整数!', u'错误', wx.OK | wx.ICON_ERROR)
        elif not is_qualified(self.field3.GetValue()):
            wx.MessageBox(u'变量个数必须为1~9整数!', u'错误', wx.OK | wx.ICON_ERROR)
        elif self.field4.GetValue() == '':
            wx.MessageBox(u'请选择保存路径!', u'错误', wx.OK | wx.ICON_ERROR)
        else:
            self.projectName = self.field1.GetValue()
            self.objectiveNumber = int(self.field2.GetValue())
            self.variableNumber = int(self.field3.GetValue())
            self.dirPath = self.field4.GetValue()
            self.Destroy()


def is_qualified(number):
    try:
        N = int(number)
        if N>0 and N<10 :
            return True
        else:
            return False
    except:
        return False
