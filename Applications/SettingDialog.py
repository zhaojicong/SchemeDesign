# -*- coding: utf-8 -*-

__author__ = 'Jack'

import wx

class SettingDialog(wx.Dialog):
    def __init__(self, parent, id=-1, title=""):
        print title
        if not title == []:
            self.algorithmInfo = title
        else:
            self.algorithmInfo = []
        wx.Dialog.__init__(self, parent, id, title=u'优化算法', size=(400, 250))
        self.InitUI()

    def InitUI(self):
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        algorithmBox = wx.StaticBox(self, label=u'算法', size=(300,250))
        algorithmBoxSizer = wx.StaticBoxSizer(algorithmBox, wx.HORIZONTAL)
        self.Algorithms = [u'遗传算法', u'模拟退火算法', u'基向量算法']
        if not self.algorithmInfo == []:
            if self.algorithmInfo[0] == 'Genetic Algorithm':
                value = u'遗传算法'
            elif self.algorithmInfo[0] == 'Simulated Anealing':
                value = u'模拟退火算法'
            elif self.algorithmInfo[0] == 'Vector Base':
                value = u'基向量算法'
            self.cb = wx.ComboBox(self, choices=self.Algorithms, style=wx.CB_READONLY,
                                  name='Algorithm', value=value, size=(200, 40))
            optionbutton = wx.Button(self, label=u'选项', id=wx.ID_ANY)
        else:
            self.cb = wx.ComboBox(self, choices=self.Algorithms, style=wx.CB_READONLY,
                                  name='Algorithm', size=(200, 40))
            optionbutton = wx.Button(self, label=u'选项', id=wx.ID_ANY, size=(80, 40))

        self.Bind(wx.EVT_BUTTON, self.OnOption, optionbutton)

        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        okbutton = wx.Button(self, label=u'确定', id=wx.ID_OK)
        cancelbutton = wx.Button(self, label=u'取消', id=wx.ID_CANCEL)
        buttonSizer.Add(okbutton, 0, wx.ALL, 8)
        buttonSizer.Add(cancelbutton, 0, wx.ALL, 8)
        algorithmBoxSizer.Add(self.cb, 0, wx.ALL, 8)
        algorithmBoxSizer.Add(optionbutton, 0, wx.ALL, 8)

        self.Bind(wx.EVT_BUTTON, self.OnOK, id=wx.ID_OK)

        mainSizer.Add(algorithmBoxSizer, flag=wx.ALIGN_CENTER|wx.ALL, border=10)
        mainSizer.Add(buttonSizer, flag=wx.ALIGN_CENTER|wx.ALL, border=8)

        self.SetSizer(mainSizer)
        self.Centre()
        self.Show(True)

    def OnOption(self, e):
        Algorithm = self.cb.GetValue()
        if Algorithm == u'遗传算法':
            if not self.algorithmInfo == []:
                gadialog = GADialog(None, title=self.algorithmInfo[1])
            else:
                gadialog = GADialog(None, title=[])
            if gadialog.ShowModal() == wx.ID_CANCEL:
                return
            if gadialog.setting != []:
                self.algorithmInfo = []
                self.algorithmInfo.append('Genetic Algorithm')
                self.algorithmInfo.append(gadialog.setting)
            print self.algorithmInfo
            gadialog.Destroy()
        elif Algorithm == u'模拟退火算法':
            sadialog = SADialog(None)
            sadialog.ShowModal()
            sadialog.Destroy()
        elif Algorithm == u'基向量算法':
            rbfdialog = RBFDialog(None)
            rbfdialog.ShowModal()
            rbfdialog.Destroy()
        else:
            wx.MessageBox(u'请先选择一个优化算法', u'提示', wx.OK | wx.ICON_INFORMATION)

    def OnOK(self, e):
        if len(self.algorithmInfo) != 2:
            wx.MessageBox(u'算法设置没有完成，请设置算法。', u'提示', wx.OK | wx.ICON_INFORMATION)
        else:
            print u'算法设置完成'
            self.Destroy()

class GADialog(wx.Dialog):
    def __init__(self, parent, id=-1, title=""):
        if not title == []:
            self.option = title
        else:
            self.option = []
        wx.Dialog.__init__(self, parent, id, title=u'遗传算法', size=(400, 550))
        self.setting = []
        self.InitUI()

    def InitUI(self):
        panel = wx.Panel(self)
        groupsizelabel1 = wx.StaticText(panel, label=u'种群数量：', pos=(20, 20))
        self.groupsizelabel2 = wx.StaticText(panel, label='100', pos=(200, 20))
        groupsizeslider = wx.Slider(panel, value=100, minValue=50, maxValue=500, pos=(50, 70),
                                    size=(250, -1), style=wx.SL_HORIZONTAL)
        iterationlabel1 = wx.StaticText(panel, label=u'迭代次数: ', pos=(20, 120))
        self.iterationlabel2 = wx.StaticText(panel, label='50', pos=(200, 120))
        iterationslider = wx.Slider(panel, value=50, minValue=10, maxValue=100, pos=(50, 170),
                                    size=(250, -1), style=wx.SL_HORIZONTAL)
        pcrossoverlabel1 = wx.StaticText(panel, label=u'重组概率: ', pos=(20, 220))
        self.pcrossoverlabel2 = wx.StaticText(panel, label='0.4', pos=(200, 220))
        pcrossoverslider = wx.Slider(panel, value=4, minValue=1, maxValue=9, pos=(50, 270),
                                    size=(250, -1), style=wx.SL_HORIZONTAL)
        pmutationlabel1 = wx.StaticText(panel, label=u'变异概率: ', pos=(20, 320))
        self.pmutationlabel2 = wx.StaticText(panel, label='0.05', pos=(200, 320))
        pmutationslider = wx.Slider(panel, value=5, minValue=1, maxValue=10, pos=(50, 370),
                                    size=(250, -1), style=wx.SL_HORIZONTAL)
        groupsizeslider.Bind(wx.EVT_SCROLL, self.GroupSizeScroll)
        iterationslider.Bind(wx.EVT_SCROLL, self.IterationScroll)
        pcrossoverslider.Bind(wx.EVT_SCROLL, self.PcrossoverScroll)
        pmutationslider.Bind(wx.EVT_SCROLL, self.PmutationScroll)

        if not self.option == []:
            self.groupsizelabel2.SetLabel(str(self.option[0]))
            self.iterationlabel2.SetLabel(str(self.option[1]))
            self.pcrossoverlabel2.SetLabel(str(self.option[2]))
            self.pmutationlabel2.SetLabel(str(self.option[3]))
            groupsizeslider.SetValue(self.option[0])
            iterationslider.SetValue(self.option[1])
            pcrossoverslider.SetValue(int(10*self.option[2]))
            pmutationslider.SetValue(int(100*self.option[3]))

        okbutton = wx.Button(panel, label=u'确定', id=wx.ID_OK, pos=(50, 400))
        cancelbutton = wx.Button(panel, label=u'取消', id=wx.ID_CANCEL, pos=(200, 400))
        self.Bind(wx.EVT_BUTTON, self.OnOK, id=wx.ID_OK)
        self.Centre()
        self.Show(True)

    def GroupSizeScroll(self, e):
        obj = e.GetEventObject()
        val = obj.GetValue()
        self.groupsizelabel2.SetLabel(str(val))

    def IterationScroll(self, e):
        obj = e.GetEventObject()
        val = obj.GetValue()
        self.iterationlabel2.SetLabel(str(val))

    def PcrossoverScroll(self, e):
        obj = e.GetEventObject()
        val = obj.GetValue()
        self.pcrossoverlabel2.SetLabel(str(val/10.0))

    def PmutationScroll(self, e):
        obj = e.GetEventObject()
        val = obj.GetValue()
        self.pmutationlabel2.SetLabel(str(val/100.0))

    def OnOK(self, e):
        self.setting = []
        self.setting.append(int(self.groupsizelabel2.GetLabel()))
        self.setting.append(int(self.iterationlabel2.GetLabel()))
        self.setting.append(float(self.pcrossoverlabel2.GetLabel()))
        self.setting.append(float(self.pmutationlabel2.GetLabel()))
        self.Destroy()

class SADialog(wx.Dialog):
    def __init__(self, parent, id=-1, title="Simulated Annealing"):
        wx.Dialog.__init__(self, parent, id, title, size=(400, 800))
        self.InitUI()

    def InitUI(self):
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self)

        mainSizer.Add(panel, 0, wx.ALL, 8)

        self.SetSizer(mainSizer)
        self.Centre()
        self.Show(True)

class RBFDialog(wx.Dialog):
    def __init__(self, parent, id=-1, title="Radial Basis Function"):
        wx.Dialog.__init__(self, parent, id, title, size=(400, 800))
        self.InitUI()

    def InitUI(self):
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self)

        mainSizer.Add(panel, 0, wx.ALL, 8)

        self.SetSizer(mainSizer)
        self.Centre()
        self.Show(True)

def isint(number):
    try:
        int(number)
        return True
    except:
        return False



