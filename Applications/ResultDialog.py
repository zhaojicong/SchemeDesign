# -*- coding: utf-8 -*-

__author__ = 'Jack'

import wx
import wx.grid

class ResultDialog(wx.Dialog):
    def __init__(self, parent, id=-1, title=""):
        result = title.__getitem__('result')
        objectivenames = title.__getitem__('objectivenames')
        objectivenumber = len(objectivenames)
        variablenames = title.__getitem__('variablenames')
        variablenumber = len(variablenames)
        wx.Dialog.__init__(self, parent, id, title=u'结果', size=[600, 600],
                           style=wx.DEFAULT_DIALOG_STYLE|wx.THICK_FRAME|wx.RESIZE_BORDER|wx.TAB_TRAVERSAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        panel = wx.Panel(self, -1)
        self.grid = MyGrid(panel)
        row = 1+len(result)
        col = 1+variablenumber+objectivenumber
        self.grid.CreateGrid(row, col)
        print 'row', row
        print 'col', col
        for i in range(0, row):
            for j in range(0, col):
                if i == 0:
                    if j == 0:
                        self.grid.SetCellValue(i, j, u'序号')
                    if 0 < j < 1+objectivenumber:
                        self.grid.SetCellValue(i, j, u'目标 - '+objectivenames[j-1])
                    if j > variablenumber:
                        self.grid.SetCellValue(i, j, u'变量 - '+variablenames[j-objectivenumber-1])
                else:
                    if j == 0:
                        self.grid.SetCellValue(i, j, str(i))
                    if 0 < j < 1+variablenumber:
                        self.grid.SetCellValue(i, j, str(result[i-1][j-1]))
                    if j > variablenumber:
                        self.grid.SetCellValue(i, j, str(result[i-1][j-objectivenumber-1]))

        mainsizer = wx.BoxSizer(wx.VERTICAL)
        mainsizer.Add(self.grid, 1, wx.EXPAND, 5)
        panel.SetSizer(mainsizer)
        self.Centre()

class MyGrid(wx.grid.Grid):
    """ A Copy&Paste enabled grid class"""
    def __init__(self, parent):
        wx.grid.Grid.__init__(self, parent)
        wx.EVT_KEY_DOWN(self, self.OnKey)
        self.data4undo = [0, 0, '']

    def OnKey(self, event):
        # If Ctrl+C is pressed...
        if event.ControlDown() and event.GetKeyCode() == 67:
            self.copy()
        # If Ctrl+V is pressed...
        if event.ControlDown() and event.GetKeyCode() == 86:
            self.paste('clip')
        # If Ctrl+Z is pressed...
        if event.ControlDown() and event.GetKeyCode() == 90:
            if self.data4undo[2] != '':
                self.paste('undo')
        # If del is pressed...
        if event.GetKeyCode() == 127:
            # Call delete method
            self.delete()
        # Skip other Key events
        if event.GetKeyCode():
            event.Skip()
            return

    def copy(self):
        # Number of rows and cols

        if self.GetSelectionBlockTopLeft() == []:
            rows = 1
            cols = 1
            iscell = True
        else:
            rows = self.GetSelectionBlockBottomRight()[0][0] - self.GetSelectionBlockTopLeft()[0][0] + 1
            cols = self.GetSelectionBlockBottomRight()[0][1] - self.GetSelectionBlockTopLeft()[0][1] + 1
            iscell = False
        # data variable contain text that must be set in the clipboard
        data = ''
        # For each cell in selected range append the cell value in the data variable
        # Tabs '\t' for cols and '\r' for rows
        for r in range(rows):
            for c in range(cols):
                if iscell:
                    data += str(self.GetCellValue(self.GetGridCursorRow() + r, self.GetGridCursorCol() + c))
                else:
                    data += str(self.GetCellValue(self.GetSelectionBlockTopLeft()[0][0] + r, self.GetSelectionBlockTopLeft()[0][1] + c))
                if c < cols - 1:
                    data += '\t'
            data += '\n'
        # Create text data object
        clipboard = wx.TextDataObject()
        # Set data object value
        clipboard.SetText(data)
        # Put the data in the clipboard
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(clipboard)
            wx.TheClipboard.Close()
        else:
            wx.MessageBox("Can't open the clipboard", "Error")

    def paste(self, stage):
        if stage == 'clip':
            clipboard = wx.TextDataObject()
            if wx.TheClipboard.Open():
                wx.TheClipboard.GetData(clipboard)
                wx.TheClipboard.Close()
            else:
                wx.MessageBox("Can't open the clipboard", "Error")
            data = clipboard.GetText()
            if self.GetSelectionBlockTopLeft() == []:
                rowstart = self.GetGridCursorRow()
                colstart = self.GetGridCursorCol()
            else:
                rowstart = self.GetSelectionBlockTopLeft()[0][0]
                colstart = self.GetSelectionBlockTopLeft()[0][1]
        elif stage == 'undo':
            data = self.data4undo[2]
            rowstart = self.data4undo[0]
            colstart = self.data4undo[1]
        else:
            wx.MessageBox("Paste method "+stage+" does not exist", "Error")
        text4undo = ''
        # Convert text in a array of lines
        for y, r in enumerate(data.splitlines()):
            # Convert c in a array of text separated by tab
            for x, c in enumerate(r.split('\t')):
                if y + rowstart < self.NumberRows and x + colstart < self.NumberCols :
                    text4undo += str(self.GetCellValue(rowstart + y, colstart + x)) + '\t'
                    self.SetCellValue(rowstart + y, colstart + x, c)
            text4undo = text4undo[:-1] + '\n'
        if stage == 'clip':
            self.data4undo = [rowstart, colstart, text4undo]
        else:
            self.data4undo = [0, 0, '']

    def delete(self):
        # print "Delete method"
        # Number of rows and cols
        if self.GetSelectionBlockTopLeft() == []:
            rows = 1
            cols = 1
        else:
            rows = self.GetSelectionBlockBottomRight()[0][0] - self.GetSelectionBlockTopLeft()[0][0] + 1
            cols = self.GetSelectionBlockBottomRight()[0][1] - self.GetSelectionBlockTopLeft()[0][1] + 1
        # Clear cells contents
        for r in range(rows):
            for c in range(cols):
                if self.GetSelectionBlockTopLeft() == []:
                    self.SetCellValue(self.GetGridCursorRow() + r, self.GetGridCursorCol() + c, '')
                else:
                    self.SetCellValue(self.GetSelectionBlockTopLeft()[0][0] + r, self.GetSelectionBlockTopLeft()[0][1] + c, '')




