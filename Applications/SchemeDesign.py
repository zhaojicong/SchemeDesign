# -*- coding: utf-8 -*-

__author__ = 'Jack'
import os
import wx
from wx.lib.buttons import GenBitmapTextButton
from wx.lib.analogclock.lib_setup.buttontreectrlpanel import ButtonTreeCtrlPanel
import time
import codecs
import threading
from NewDialog import *
from TargetDialog import *
from ObjectiveDialog import *
from VariableDialog import *
from CheckDialog import *
from SettingDialog import *
from ResultDialog import *
from ChartDialog import *
from Calculation import *




class SchemeDesign(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(SchemeDesign, self).__init__(*args, **kwargs)

        self.InitUI()
        self.projectName = None
        self.objectiveNumber = 0
        self.variableNumber = 0
        self.schemeNumber = 0
        self.targetButton = None
        self.objectiveButtons = []
        self.variableButtons = []
        self.objectiveNames = []
        self.variableNames = []
        self.objectives = {} # name to function (name, 'function')
        self.variables = {}  # name to boundary (name, str(lowerbound)+','+str(upperbound))
        self.algorithmInfo = []
        self.d ={}
        self.result = []
        self.contentNotSaved = False
        self.fileDir = None
        self.filePath = None
        self.resultPath = None
        self.fileName = None

    def InitParameter(self):
        self.projectName = None
        self.objectiveNumber = 0
        self.variableNumber = 0
        self.schemeNumber = 0
        self.targetButton = None
        self.objectiveButtons = []
        self.variableButtons = []
        self.objectiveNames = []
        self.variableNames = []
        self.objectives = {}  # name to function (name, 'function')
        self.variables = {}  # name to boundary (name, str(lowerbound)+','+str(upperbound))
        self.algorithmInfo = []
        self.d ={}
        self.result = []
        self.contentNotSaved = False
        self.fileDir = None
        self.filePath = None
        self.resultPath = None
        self.fileName = None

    def InitUI(self):

        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        editMenu = wx.Menu()
        solveMenu = wx.Menu()
        viewMenu = wx.Menu()
        helpMenu = wx.Menu()
        importMenu = wx.Menu()

        newitem = wx.MenuItem(fileMenu, wx.ID_NEW, u'&新建\tCtrl+N')
        openitem = wx.MenuItem(fileMenu, wx.ID_OPEN, u'&打开\tCtrl+O')
        saveitem = wx.MenuItem(fileMenu, wx.ID_SAVE, u'&保存\tCtrl+S')
        saveasitem = wx.MenuItem(fileMenu, wx.ID_SAVEAS, u'另存为\tCtrl+A')
        importresult = wx.MenuItem(fileMenu, wx.ID_ANY,u'导入结果\tCtrl+R')
        quititem = wx.MenuItem(fileMenu, wx.ID_EXIT, u'&退出\tCtrl+Q')
        drawitem = wx.MenuItem(viewMenu, wx.ID_ANY, u'&连线\tCtrl+D')
        checkitem = wx.MenuItem(solveMenu, wx.ID_ANY, u'&查看参数\tCtrl+Alt+C')
        settingitem = wx.MenuItem(solveMenu, wx.ID_ANY, u'&算法设置\tCtrl+Alt+S')
        startitem = wx.MenuItem(solveMenu, wx.ID_ANY, u'&开始计算\tCtrl+Alt+T')
        resultitem = wx.MenuItem(solveMenu, wx.ID_ANY, u'&查看结果\tCtrl+Alt+R')
        chartitem = wx.MenuItem(solveMenu, wx.ID_ANY, u'&图形展示\tCtrl+Alt+H')
        helpitem = wx.MenuItem(helpMenu, wx.ID_HELP, u'&帮助\tCtrl+Alt+H')
        aboutitem = wx.MenuItem(helpMenu, wx.ID_ABOUT, u'&关于我们\tCtrl+B')

        fileMenu.AppendItem(newitem)
        fileMenu.AppendItem(openitem)
        fileMenu.AppendItem(saveitem)
        fileMenu.AppendItem(saveasitem)
        importMenu.AppendItem(importresult)
        fileMenu.AppendMenu(wx.ID_ANY, u'导入', importMenu)
        fileMenu.AppendSeparator()
        fileMenu.AppendItem(quititem)
        viewMenu.AppendItem(drawitem)
        helpMenu.AppendItem(helpitem)
        helpMenu.AppendItem(aboutitem)
        solveMenu.AppendItem(checkitem)
        solveMenu.AppendItem(settingitem)
        solveMenu.AppendItem(startitem)
        solveMenu.AppendItem(resultitem)
        solveMenu.AppendItem(chartitem)

        menubar.Append(fileMenu, u'&文件')
        menubar.Append(editMenu, u'&编辑')
        menubar.Append(viewMenu, u'&查看')
        menubar.Append(solveMenu, u'&求解')
        menubar.Append(helpMenu, u'&帮助')
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.OnQuit, quititem)
        self.Bind(wx.EVT_MENU, self.OnNew, newitem)
        self.Bind(wx.EVT_MENU, self.OnOpen, openitem)
        self.Bind(wx.EVT_MENU, self.OnSave, saveitem)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, saveasitem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutitem)
        self.Bind(wx.EVT_MENU, self.OnPaint, drawitem)
        self.Bind(wx.EVT_MENU, self.OnCheck, checkitem)
        self.Bind(wx.EVT_MENU, self.OnStart, startitem)
        self.Bind(wx.EVT_MENU, self.OnSetting, settingitem)
        self.Bind(wx.EVT_MENU, self.OnResult, resultitem)
        self.Bind(wx.EVT_MENU, self.OnImportResult, importresult)

        toolbar = wx.ToolBar(self, style=wx.TB_TEXT)
        newtool = toolbar.AddLabelTool(id=wx.ID_ANY, label=u'新建', bitmap=wx.Bitmap('image/toolbar/new.png', wx.BITMAP_TYPE_PNG), shortHelp=u'新建')
        opentool = toolbar.AddLabelTool(id=wx.ID_ANY, label=u'打开', bitmap=wx.Bitmap('image/toolbar/open.png', wx.BITMAP_TYPE_PNG), shortHelp=u'打开')
        savetool = toolbar.AddLabelTool(id=wx.ID_ANY, label=u'保存', bitmap=wx.Bitmap('image/toolbar/save.png', wx.BITMAP_TYPE_PNG), shortHelp=u'保存')
        saveastool = toolbar.AddLabelTool(id=wx.ID_ANY, label=u'另存为', bitmap=wx.Bitmap('image/toolbar/saveas.png', wx.BITMAP_TYPE_PNG), shortHelp=u'另存为')
        toolbar.AddSeparator()
        checktool = toolbar.AddLabelTool(id=wx.ID_ANY, label=u'检查', bitmap=wx.Bitmap('image/toolbar/check.png', wx.BITMAP_TYPE_PNG), shortHelp=u'查看参数')
        settingktool = toolbar.AddLabelTool(id=wx.ID_ANY, label=u'算法', bitmap=wx.Bitmap('image/toolbar/setting.png', wx.BITMAP_TYPE_PNG), shortHelp=u'算法设置')
        starttool = toolbar.AddLabelTool(id=wx.ID_ANY, label=u'开始', bitmap=wx.Bitmap('image/toolbar/start.png', wx.BITMAP_TYPE_PNG), shortHelp=u'开始计算')
        resulttool = toolbar.AddLabelTool(id=wx.ID_ANY, label=u'结果', bitmap=wx.Bitmap('image/toolbar/result.png', wx.BITMAP_TYPE_PNG), shortHelp=u'结果')
        charttool = toolbar.AddLabelTool(id=wx.ID_ANY, label=u'作图', bitmap=wx.Bitmap('image/toolbar/chart.png',wx.BITMAP_TYPE_PNG), shortHelp=u'图形展示')
        toolbar.AddSeparator()
        helptool = toolbar.AddLabelTool(id=wx.ID_ANY, label=u'帮助', bitmap=wx.Bitmap('image/toolbar/help.png', wx.BITMAP_TYPE_PNG), shortHelp=u'帮助')
        infotool = toolbar.AddLabelTool(id=wx.ID_ANY, label=u'关于', bitmap=wx.Bitmap('image/toolbar/info.png', wx.BITMAP_TYPE_PNG), shortHelp=u'关于我们')
        quittool = toolbar.AddLabelTool(id=wx.ID_ANY, label=u'退出', bitmap=wx.Bitmap('image/toolbar/quit.png', wx.BITMAP_TYPE_PNG), shortHelp=u'退出')
        toolbar.Realize()
        self.Bind(wx.EVT_TOOL, self.OnQuit, quittool)
        self.Bind(wx.EVT_TOOL, self.OnNew, newtool)
        self.Bind(wx.EVT_TOOL, self.OnHelp, helptool)
        self.Bind(wx.EVT_TOOL, self.OnAbout, infotool)
        self.Bind(wx.EVT_TOOL, self.OnCheck, checktool)
        self.Bind(wx.EVT_TOOL, self.OnSetting, settingktool)
        self.Bind(wx.EVT_TOOL, self.OnStart, starttool)
        self.Bind(wx.EVT_TOOL, self.OnOpen, opentool)
        self.Bind(wx.EVT_TOOL, self.OnSave, savetool)
        self.Bind(wx.EVT_TOOL, self.OnResult, resulttool)
        self.Bind(wx.EVT_TOOL, self.OnSaveAs, saveastool)
        self.Bind(wx.EVT_TOOL, self.OnChart, charttool)

        self.Maximize(True)

        self.SetTitle(u'方案设计与优化')
        self.Centre()
        self.Show(True)

    def OnHelp(self, e):
        self.Close()

    def OnQuit(self, e):
        if self.contentNotSaved:
            messagebox = wx.MessageBox(u'当前内容没有保存，是否继续退出？', u'方案设计与优化',
                                       wx.ICON_WARNING|wx.YES_NO, self)
            if messagebox == wx.NO or messagebox == wx.CANCEL:
                return
            if messagebox == wx.YES:
                self.Destroy()
        else:
            self.Destroy()

    def OnNew(self, e):
        if self.projectName == None:
            newdialog = NewDialog(None)
            if newdialog.ShowModal() == wx.ID_CANCEL:
                return
            self.projectName = newdialog.projectName
            self.objectiveNumber = newdialog.objectiveNumber
            self.variableNumber = newdialog.variableNumber
            self.fileDir = newdialog.dirPath
            print "Project Name:", self.projectName
            print "Objective Number:", self.objectiveNumber
            print "Variable Number:", self.variableNumber
            print 'Saving path:', unicode(self.fileDir)
            newdialog.Destroy()
            self.InitFrame()
            self.contentNotSaved = True
        else:
            newdialog = NewDialog(None)
            if newdialog.ShowModal() == wx.ID_CANCEL:
                return
            newwindow = SchemeDesign(None)
            newwindow.projectName = newdialog.projectName
            newwindow.objectiveNumber = newdialog.objectiveNumber
            newwindow.variableNumber = newdialog.variableNumber
            print "Project Name:", newwindow.projectName
            print "Objective Number:", newwindow.objectiveNumber
            print "Variable Number:", newwindow.variableNumber
            print 'Saving path: ', unicode(newwindow.fileDir)
            newdialog.Destroy()
            newwindow.InitFrame()
            newwindow.contentNotSaved = True

    def InitFrame(self):
        panel = wx.Panel(self, size=(2000, 1000), pos=(0, 70))
        bmp = wx.Bitmap('image/button/target.png', wx.BITMAP_TYPE_PNG)
        self.targetButton = GenBitmapTextButton(panel, bitmap=bmp, label=self.projectName, name=self.projectName, pos=(300, 300))
        for i in range(0, self.objectiveNumber):
            bmp = wx.Bitmap('image/button/objective.png', wx.BITMAP_TYPE_PNG)
            distance = 800/(self.objectiveNumber+2)
            if len(self.objectiveNames) == self.objectiveNumber:
                button = GenBitmapTextButton(panel, label=self.objectiveNames[i], bitmap=bmp, name=self.objectiveNames[i], pos=(600, distance*(i+1)))
                self.objectiveButtons.append(button)
            else:
                button = GenBitmapTextButton(panel, bitmap=bmp, label='Objective_'+str(i+1),name='Objective_'+str(i+1), pos=(600, distance*(i+1)))
                self.objectiveButtons.append(button)
                self.objectiveNames.append('Objective_'+str(i+1))
        for i in range(0, self.variableNumber):
            bmp = wx.Bitmap('image/button/variable.png', wx.BITMAP_TYPE_PNG)
            distance = 800/(self.variableNumber+2)
            if len(self.variableNames) == self.variableNumber:
                button = GenBitmapTextButton(panel, bitmap=bmp, label=self.variableNames[i], name=self.variableNames[i], pos=(900, distance*(i+1)))
                self.variableButtons.append(button)
            else:
                button = GenBitmapTextButton(panel, bitmap=bmp, label='Variable_'+str(i+1), name='Variable_'+str(i+1), pos=(900, distance*(i+1)))
                self.variableButtons.append(button)
                self.variableNames.append('Variable_'+str(i+1))
        panel.SetBackgroundColour(wx.WHITE)
        panel.Layout()

        # Binding buttons with dialog
        self.targetButton.Bind(wx.EVT_BUTTON, self.OnTargetButton)
        self.targetButton.Bind(wx.EVT_RIGHT_DOWN, self.MouseDown)
        self.targetButton.Bind(wx.EVT_MOTION, self.MouseMove)
        self.targetButton.Bind(wx.EVT_RIGHT_UP, self.MouseUp)
        for button in self.objectiveButtons:
            button.Bind(wx.EVT_BUTTON, self.OnObjectiveButton)
            button.Bind(wx.EVT_RIGHT_DOWN, self.MouseDown)
            button.Bind(wx.EVT_MOTION, self.MouseMove)
            button.Bind(wx.EVT_RIGHT_UP, self.MouseUp)
        for button in self.variableButtons:
            button.Bind(wx.EVT_BUTTON, self.OnVariableButton)
            button.Bind(wx.EVT_RIGHT_DOWN, self.MouseDown)
            button.Bind(wx.EVT_MOTION, self.MouseMove)
            button.Bind(wx.EVT_RIGHT_UP, self.MouseUp)
        if self.filePath is None:
            self.SetTitle(self.projectName+u' - 方案设计与优化')
        else:
            name = self.filePath.split('\\')
            self.SetTitle(name[-1]+u' - 方案设计与优化')

    def OnOpen(self, e):
        if self.fileDir is not None:
            openFileDialog = wx.FileDialog(self, u'请选择sdp文件', unicode(self.fileDir), '', u'sdp文件 (*.sdp)|*.sdp', wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        else:
            openFileDialog = wx.FileDialog(self, u'请选择sdp文件', '', '', u'sdp文件 (*.sdp)|*.sdp', wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return     # the user changed idea...
        if self.projectName is not None:
            newwindow = SchemeDesign(None)
            newwindow.filePath = openFileDialog.GetPath()
            newwindow.fileDir = openFileDialog.GetDirectory()
            newwindow.fileName = openFileDialog.GetFilename()
            try:
                file = open(newwindow.filePath)
                for line in file:
                    sline = line.split(':')
                    print line
                    if sline[0].strip() == 'project name':
                        newwindow.projectName = sline[1].strip()
                        print newwindow.projectName
                    if sline[0].strip() == 'objective':
                        newwindow.objectiveNumber += 1
                        objective = sline[1].split(',')
                        newwindow.objectiveNames.append(objective[0].strip())
                        if objective[1].strip() == 'min':
                            newwindow.objectives.__setitem__(objective[0].strip(), objective[2].strip())
                        elif objective[1].strip() == 'max':
                            newwindow.objectives.__setitem__(objective[0].strip(), '-1*('+objective[2].strip()+')')
                        print newwindow.objectives
                    if sline[0].strip() == 'variable':
                        newwindow.variableNumber += 1
                        variable = sline[1].split(',')
                        newwindow.variableNames.append(variable[0].strip())
                        newwindow.variables.__setitem__(variable[0].strip(), [float(variable[1].strip()), float(variable[2].strip())])
                        print newwindow.variables
                    if sline[0].strip() == 'algorithm':
                        algorithmInfo = sline[1].split(',')
                        newwindow.algorithmInfo.append(algorithmInfo[0].strip())
                        newwindow.algorithmInfo.append([int(algorithmInfo[1].strip()), int(algorithmInfo[2].strip()),
                                                        float(algorithmInfo[3].strip()), float(algorithmInfo[4].strip())])
                        print newwindow.algorithmInfo
                file.close()
                newwindow.InitFrame()
            except:
                wx.MessageBox(u'无法打开 ' + newwindow.filePath, u'打开文件错误', wx.ICON_ERROR | wx.YES_NO, self)
                return
        else:
            self.filePath = openFileDialog.GetPath()
            self.fileDir = openFileDialog.GetDirectory()
            self.fileName = openFileDialog.GetFilename()
            print self.fileName, type(self.filePath)
            try:
                file = open(self.filePath)
                for line in file:
                    sline = line.split(':')
                    print line
                    if sline[0].strip() == 'project name':
                        self.projectName = sline[1].strip()
                        print self.projectName
                    if sline[0].strip() == 'objective':
                        self.objectiveNumber += 1
                        objective = sline[1].split(',')
                        self.objectiveNames.append(objective[0].strip())
                        if objective[1].strip() == 'min':
                            self.objectives.__setitem__(objective[0].strip(), objective[2].strip())
                        elif objective[1].strip() == 'max':
                            self.objectives.__setitem__(objective[0].strip(), '-1*('+objective[2].strip()+')')
                        print self.objectives
                    if sline[0].strip() == 'variable':
                        self.variableNumber += 1
                        variable = sline[1].split(',')
                        self.variableNames.append(variable[0].strip())
                        self.variables.__setitem__(variable[0].strip(), [float(variable[1].strip()), float(variable[2].strip())])
                        print self.variables
                    if sline[0].strip() == 'algorithm':
                        algorithmInfo = sline[1].split(',')
                        self.algorithmInfo.append(algorithmInfo[0].strip())
                        self.algorithmInfo.append([int(algorithmInfo[1].strip()), int(algorithmInfo[2].strip()),
                                                        float(algorithmInfo[3].strip()), float(algorithmInfo[4].strip())])
                        print self.algorithmInfo
                file.close()
                self.InitFrame()
            except:
                wx.MessageBox(u'无法打开 ' + self.filePath, u'打开文件错误', wx.ICON_ERROR | wx.YES_NO, self)
                return

    def OnSave(self, e):
        if self.contentNotSaved == False:
            return
        elif self.filePath == None:
            e = wx.EVT_ACTIVATE
            self.OnSaveAs(e)
            return
        else:
            try:
                file = open(self.filePath, 'w+')
                file.write('project name: '+self.projectName.decode('utf-8')+'\n')
                file.write('\n')
                for name in self.objectiveNames:
                    try:
                        function = self.objectives.__getitem__(name)
                        if function.startswith('-1*(') and function.endswith(')'):
                            file.write('objective: '+name+', '+'max, '+function[4:len(function)-1])
                            file.write('\n')
                        else:
                            file.write('objective: '+name+', '+'min, '+function)
                            file.write('\n')
                    except:
                        pass
                file.write('\n')
                for name in self.variableNames:
                    try:
                        boundary = self.variables.__getitem__(name)
                        file.write('variable: '+name+', '+str(boundary[0])+', '+str(boundary[1]))
                        file.write('\n')
                    except:
                        pass
                file.write('\n')
                try:
                    if not self.algorithmInfo == []:
                        file.write('algorithm: '+self.algorithmInfo[0])
                        for parameter in self.algorithmInfo[1]:
                            file.write(', '+str(parameter))
                except:
                    pass
                file.write('\n')
                file.close()
                self.contentNotSaved = False

            except:
                print "can't save!"

    def OnSaveAs(self, e):
        if self.projectName == None:
            wx.MessageBox(u'没有项目可以保存，请先新建或打开一个项目！', u'错误', wx.OK | wx.ICON_ERROR)
            return
        saveFileDialog = wx.FileDialog(self, u'保存文件', unicode(self.fileDir), '',
                                       u"dsp文件(*.sdp)|*.sdp", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        if saveFileDialog.ShowModal() == wx.ID_CANCEL:
            return  # the user changed idea...

        # save the current contents in the file
        # this can be done with e.g. wxPython output streams:
        try:
            file = open(saveFileDialog.GetPath(), 'w+')
            self.filePath = saveFileDialog.GetPath()
            self.fileDir = saveFileDialog.GetDirectory()
            self.fileName = saveFileDialog.GetFilename()
            file.write('project name: '+self.projectName+'\n')
            file.write('\n')
            for name in self.objectiveNames:
                try:
                    function = self.objectives.__getitem__(name)
                    if function.startswith('-1*(') and function.endswith(')'):
                        file.write('objective: '+name+', '+'max, '+function[4:len(function)-1])
                        file.write('\n')
                    else:
                        file.write('objective: '+name+', '+'min, '+function)
                        file.write('\n')
                except:
                    pass
            file.write('\n')
            for name in self.variableNames:
                try:
                    boundary = self.variables.__getitem__(name)
                    file.write('variable: '+name+', '+str(boundary[0])+', '+str(boundary[1]))
                    file.write('\n')
                except:
                    pass
            file.write('\n')
            try:
                if not self.algorithmInfo == []:
                    file.write('algorithm: '+self.algorithmInfo[0])
                    for parameter in self.algorithmInfo[1]:
                        file.write(', '+str(parameter))
            except:
                pass
            file.write('\n')
            file.close()
        except:
            print "can't save!"

    def OnImportResult(self, e):
        if self.fileDir is not None:
            openFileDialog = wx.FileDialog(self, u'请选择rst文件', unicode(self.fileDir), '', u'rst文件 (*.rst)|*.rst', wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        else:
            openFileDialog = wx.FileDialog(self, u'请选择rst文件', unicode(self.fileDir), '', u'rst文件 (*.rst)|*.rst', wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return     # the user changed idea...
        self.resultPath = openFileDialog.GetPath()
        # try:
        file = open(unicode(self.resultPath), 'r')
        for line in file:
            sline = line.split('$,')
            if sline[0] == 'Order':
                self.objectiveNames = sline[1].split(',')
                self.variableNames = sline[2].split(',')
            else:
                stringresult =sline[0].split(',')
                stringresult.pop(0)
                floatresult = []
                for item in stringresult:
                    floatresult.append(float(item))
                self.result.append(floatresult)
        file.close()
        e = wx.EVT_ACTIVATE
        self.OnResult(e)
        # except:
        #     print 'Cannot open' + self.resultPath
        #     pass

    def OnTargetButton(self, e):
        button = e.GetEventObject()
        name = button.GetLabelText()
        targetdialog = TargetDialog(None, title=name)
        if targetdialog.ShowModal() == wx.ID_CANCEL:
            return
        self.projectName = targetdialog.projectName
        self.targetButton.SetLabel(self.projectName)
        targetdialog.Destroy()
        self.contentNotSaved = True

    def OnObjectiveButton(self, e):
        button = e.GetEventObject()
        index = self.objectiveButtons.index(button)
        name = button.GetLabelText()
        if name in self.objectives.keys():
            name = name + ',' + self.objectives.get(name)
        else:
            name += ','
        objectivedialog = ObjectiveDialog(None, title=name)
        if objectivedialog.ShowModal() == wx.ID_CANCEL:
            return
        button.SetLabel(objectivedialog.objectiveName)
        self.objectiveNames[index] = objectivedialog.objectiveName
        function = objectivedialog.function
        self.objectives.__setitem__(button.GetLabelText(), function)
        objectivedialog.Destroy()
        self.contentNotSaved = True

    def OnVariableButton(self, e):
        button = e.GetEventObject()
        index = self.variableButtons.index(button)
        name = button.GetLabelText()
        if name in self.variables.keys():
            boundary = self.variables.get(name)
            name = name + ',' + str(boundary[0]) + ',' + str(boundary[1])
        else:
            name += ',,'
        name = str(index+1)+','+name
        print name
        variableDialog = VariableDialog(None, title=name)
        if variableDialog.ShowModal() == wx.ID_CANCEL:
            return
        button.SetLabel(variableDialog.variableName)
        self.variableNames[index] = variableDialog.variableName
        lowerbound = variableDialog.lowerBound
        upperbound = variableDialog.upperBound
        self.variables.__setitem__(variableDialog.variableName, [float(lowerbound), float(upperbound)])
        self.contentNotSaved = True

    def OnCheck(self, e):
        if self.projectName is None:
            wx.MessageBox(u'没有项目可以查看，请先新建或打开一个项目！', u'错误', wx.OK | wx.ICON_ERROR)
            return
        else:
            info = [[self.projectName, self.objectiveNames, self.variableNames], self.objectives,
                    self.variables, self.algorithmInfo]
            checkdialog = CheckDialog(None, title=info)
            checkdialog.SetExtraStyle(wx.RESIZE_BORDER)
            checkdialog.ShowModal()
            checkdialog.Destroy()

    def OnSetting(self, e):
        if self.projectName is None:
            wx.MessageBox(u'还没有项目，请先新建或打开一个项目', u'错误', wx.OK | wx.ICON_ERROR)
        else:
            print self.algorithmInfo
            settingdialog = SettingDialog(None, title=self.algorithmInfo)
            if settingdialog.ShowModal() == wx.ID_CANCEL:
                return
            self.algorithmInfo = settingdialog.algorithmInfo
            print self.algorithmInfo
            self.contentNotSaved = True
            settingdialog.Destroy()

    def OnStart(self, e):
        if self.projectName is None:
            wx.MessageBox(u'没有项目可以计算，请先新建一个项目', u'错误', wx.OK | wx.ICON_ERROR)
            return
        for name in self.objectiveNames:
            if name not in self.objectives.keys():
                wx.MessageBox(u'还未设置目标函数'+name, u'错误', wx.OK | wx.ICON_ERROR)
                return
        else:
            for name in self.variableNames:
                if name not in self.variables.keys():
                    wx.MessageBox(u'还未设置'+name+u'的变化范围', u'错误', wx.OK | wx.ICON_ERROR)
                    return
            else:
                if len(self.algorithmInfo) != 2:
                    wx.MessageBox(u'还未设置求解算法', u'错误', wx.OK | wx.ICON_ERROR)
                    return
                else:
                    messagebox = wx.MessageBox(u'开始计算？', u'请确认', wx.ICON_INFORMATION | wx.YES_NO)
                    if messagebox == wx.NO:
                        return
                    try:
                        calculation = Calculation(self.objectives, self.variables, self.algorithmInfo)
                        thread = threading.Thread(target=calculation.Calculate, args=())
                        progressMax = calculation.object.GetIteration()
                        count = 0
                        guagedialog = wx.ProgressDialog(u'计算进度', u'剩余时间', progressMax,
                                                style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)
                        thread.start()
                        keepGoing = True
                        while keepGoing and count < progressMax:
                            time.sleep(0.01)
                            count = calculation.object.GetProcess()
                            print 'Process: ', count
                            keepGoing = guagedialog.Update(count)
                        thread.join()
                        guagedialog.Destroy()
                        self.result = calculation.ChoosePareto()
                        try:
                            print self.fileName, type(self.fileName)

                            text = self.fileName.split('.')
                            self.resultPath = unicode(self.fileDir)+'\\' + text[0]+'.rst'
                            file = open(self.resultPath, 'w+')
                            lines = []
                            line = 'Order$'
                            for name in self.objectiveNames:
                                line = line + ',' + name
                            line += '$'
                            for name in self.variableNames:
                                line = line + ',' + name
                            lines.append(line)
                            i = 1
                            for result in self.result:
                                line = str(i)
                                for number in result:
                                    line = line + ','+str(number)
                                lines.append(line)
                                i += 1
                            for line in lines:
                                print line
                                file.write(line)
                                file.write('\n')
                            file.close()
                        except:
                            wx.MessageBox(u'结果保存出错！', u'错误', wx.OK | wx.ICON_ERROR)
                            pass
                        e = wx.EVT_ACTIVATE
                        self.OnResult(e)
                    except:
                        wx.MessageBox(u'计算出错！', u'错误', wx.OK | wx.ICON_ERROR)

    def OnResult(self, e):
        if self.result == []:
            wx.MessageBox(u'没有计算结果可以展示', u'错误', wx.OK | wx.ICON_ERROR)
        else:
            title = {
                'result': self.result,
                'objectivenames': self.objectiveNames,
                'variablenames': self.variableNames
            }
            settingdialog = ResultDialog(None, title=title)
            if settingdialog.ShowModal() == wx.CANCEL:
                return
            settingdialog.Destroy()

    def OnChart(self, e):
        if self.result == []:
            wx.MessageBox(u'没有计算结果可以展示', u'错误', wx.OK | wx.ICON_ERROR)
        else:
            title = {
                'result': self.result,
                'objectivenames': self.objectiveNames,
                'variablenames': self.variableNames
            }
            chartdialog = ChartDialog(None, title=title)
            if chartdialog.ShowModal() == wx.CANCEL:
                chartdialog.app.Destroy()
                return
            chartdialog.app.Close()
            chartdialog.Destroy()

    def MouseDown(self, e):
        o           = e.GetEventObject()
        sx,sy       = self.ScreenToClient(o.GetPositionTuple())
        dx,dy       = self.ScreenToClient(wx.GetMousePosition())
        o._x,o._y   = (sx-dx, sy-dy)
        self.d['d'] = o

    def MouseMove(self, e):
        try:
            if 'd' in self.d:
                o = self.d['d']
                x, y = wx.GetMousePosition()
                o.SetPosition(wx.Point(x+o._x,y+o._y))
        except: pass

    def MouseUp(self, e):
        try:
            if 'd' in self.d: del self.d['d']
        except: pass

    def OnAbout(self, e):

        description = ""u'方案设计与优化是针对多目标优化的软件工具。……'""

        licence = ""u'版权'""

        info = wx.AboutDialogInfo()
        info.SetName(u'方案设计与优化')
        info.SetVersion('1.0')
        info.SetDescription(description)
        info.SetCopyright(u'(C) 2015 Jicong Zhao')
        info.SetLicence(licence)
        info.AddDeveloper(u'赵继丛')
        info.AddDocWriter(u'赵继丛')

        wx.AboutBox(info)

ex = wx.App()
SchemeDesign(None)
ex.MainLoop()

