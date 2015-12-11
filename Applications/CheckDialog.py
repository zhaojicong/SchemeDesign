# -*- coding: utf-8 -*-

__author__ = 'Jack'

import wx

class CheckDialog(wx.Dialog):
    def __init__(self, parent, id=-1, title=""):
        self.info = title
        print self.info[0][0]
        wx.Dialog.__init__(self, parent, id, title=u'查看参数', size=(500, 1000),
                           style=wx.DEFAULT_DIALOG_STYLE|wx.THICK_FRAME|wx.RESIZE_BORDER|wx.TAB_TRAVERSAL)
        self.initUI()

    def initUI(self):
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        panel1 = wx.Panel(self)
        panel2 = wx.Panel(self)
        panel3 = wx.Panel(self)
        pnlabel = wx.StaticText(self, label=u'项目名称: '+self.info[0][0])
        # objective function box
        ofb = wx.StaticBox(panel1, label=u'目标函数')
        # variable boundary box
        vbb = wx.StaticBox(panel2, label=u'可调变量')
        ai = wx.StaticBox(panel3, label=u'算法信息')
        ofbSizer = wx.StaticBoxSizer(ofb, wx.VERTICAL)
        vbbSizer = wx.StaticBoxSizer(vbb, wx.VERTICAL)
        aiSizer = wx.StaticBoxSizer(ai, wx.VERTICAL)
        oflabels = []
        vblabels = []
        ailabels = []
        for name in self.info[0][1]:
            if name in self.info[1].keys():
                oflabeli = wx.StaticText(panel1, label=name+'='+self.info[1].get(name))
                print name+'='+self.info[1].get(name)
            else:
                oflabeli = wx.StaticText(panel1, label=name+u'未设置')
                print name+'=None'
            oflabels.append(oflabeli)
        i = 0
        for name in self.info[0][2]:
            i += 1
            if name in self.info[2].keys():
                vnlabel = wx.StaticText(panel2, label=u'变量x'+str(i)+u'：'+name)
                bounds = self.info[2].get(name)
                lblabel = wx.StaticText(panel2, label=u'上边界：'+str(bounds[0]))
                ublabel = wx.StaticText(panel2, label=u'下边界：'+str(bounds[1]))
            else:
                vnlabel = wx.StaticText(panel2, label=u'变量'+str(i)+u'：'+name)
                lblabel = wx.StaticText(panel2, label=u'未设置变化范围')
            vblabels.append([vnlabel, lblabel, ublabel])
        if self.info[3] == []:
            ailabels.append(wx.StaticText(panel3, label=u'没有设置算法'))
        elif self.info[3][0] == 'Genetic Algorithm':
            ailabels.append(wx.StaticText(panel3, label=u'名称: 遗传算法'))
            ailabels.append(wx.StaticText(panel3, label=u'种群数量:         '+str(self.info[3][1][0])))
            ailabels.append(wx.StaticText(panel3, label=u'迭代次数:         '+str(self.info[3][1][1])))
            ailabels.append(wx.StaticText(panel3, label=u'基因重组概率:     '+str(self.info[3][1][1])))
            ailabels.append(wx.StaticText(panel3, label=u'基因变异概率:     '+str(self.info[3][1][1])))

        for label in oflabels:
            ofbSizer.Add(label, 0, wx.ALL, 8)
        for labels in vblabels:
            for label in labels:
                vbbSizer.Add(label, 0, wx.ALL, 8)
        for label in ailabels:
            aiSizer.Add(label, 0, wx.ALL, 8)

        panel1.SetSizer(ofbSizer)
        panel2.SetSizer(vbbSizer)
        panel3.SetSizer(aiSizer)

        mainSizer.Add(pnlabel, flag=wx.EXPAND|wx.ALL, border=8)
        mainSizer.Add(panel1, flag=wx.EXPAND|wx.ALL, border=8)
        mainSizer.Add(panel2, flag=wx.EXPAND|wx.ALL, border=8)
        mainSizer.Add(panel3, flag=wx.EXPAND|wx.ALL, border=8)
        mainSizer.Add(wx.Button(self, id=wx.ID_CANCEL, label=u'返回'), flag=wx.ALIGN_CENTER, border=8)
        self.SetSizer(mainSizer)
        self.Centre()


