try:
        import wx
        import wx.grid as gridlib
except ImportError:
    raise ImportError("wxpython module required!")
try:
        import svd_PI_finder as PI
except ImportError:
    raise ImportError("PI_Finder module required!")
    
from pandas import *
from itertools import *

import numpy as np

class Pi_interface(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(800, 700))
        self.parent = parent
        self.updating_columns = False
        
        self.initialize()

    def initialize(self):

        panel = wx.Panel(self, 1, (10, 20), style=wx.SUNKEN_BORDER)
        
        menu = wx.MenuBar()
        filemenu = wx.Menu()
        fileopen = filemenu.Append(wx.ID_OPEN, '&Import', 'Import Variable Data')
        filesave = filemenu.Append(wx.ID_SAVE, '&Save', 'Save Variable and Pi Group Data')
        filemenu.AppendSeparator()
        filereset = filemenu.Append(wx.ID_RESET, '&Reset', 'Clear all data and reset fields')
        filemenu.AppendSeparator()
        filequit = filemenu.Append(wx.ID_EXIT, 'Quit', 'Close Pi Finder')
        
        menu.Append(filemenu,  '&File')
        self.SetMenuBar(menu)        
        
        self.Bind(wx.EVT_MENU, self.reset, filereset)
        self.Bind(wx.EVT_MENU, self.quit, filequit)         
        
        self.Button_permute = wx.Button(panel,-1,"Permute Pi Groups", (605,30))         
        

        ColLabels = ["Name", "L", "T", "M", u"\u03F4", "N", "I", "J"]

        Ncols = len(ColLabels)
        Nrows_initial = 1

        self.values = gridlib.Grid(panel)
        self.values.CreateGrid(Nrows_initial, Ncols)
        self.values.SetSize((600, 300))

        self.values.Bind(gridlib.EVT_GRID_CELL_CHANGE, self.OnCellChange,)
        self.Button_permute.Bind(wx.EVT_BUTTON, self.permute)

        for column, name in enumerate(ColLabels):
            self.values.SetColLabelValue(column, name)

        self.values.AutoSizeColumns()

        for r in range(Nrows_initial):
            for c in range(8, Ncols):
                self.values.SetReadOnly(r, c)
        

    def OnCellChange(self, event):
        if self.updating_columns:
            return   
        
              
        Nrows = self.values.GetNumberRows()
        Ncols = self.values.GetNumberCols()

        rcount = 0

        for r in range(0,Nrows):
            val = self.values.GetCellValue(r, 0)
            if val != '':
                rcount += 1
        
        self.input_mat = np.zeros([rcount,7]).T
        

        for update_col in range(1, 7):
            for update_row in range(0,rcount):
                val = self.values.GetCellValue(update_row, update_col)
                if val!= '':
                    self.input_mat[update_col-1,update_row] = val            
        if Nrows > 1:
            self.input_fixed = self.input_mat[self.input_mat.any(1)].T
            self.Result = PI.buck(self.input_fixed)        
        
        if Nrows > 2 :
           val = self.values.GetCellValue(Nrows-2, 0) 
           if val == '':
                self.updating_columns = True
                self.values.DeleteRows(Nrows-2)
                self.updating_columns = False
                
        val = self.values.GetCellValue(Nrows-1, 0)    
        
        if val != '':
            self.updating_columns = True
            self.values.InsertRows(Nrows, 1)
            self.updating_columns = False

            for entry_row_check in range(0, Nrows):
                for add in range(1, 8):
                    val = self.values.GetCellValue(entry_row_check, add)
                    if val == '' or val == '0':
                        self.values.SetCellValue(entry_row_check, add, '0')
            
        if self.Result != None:   
            [res_rows, res_cols] = self.Result.shape
            self.Permute_Result = np.matrix(np.zeros([res_rows,1]))
        else:
            res_cols = 0
            res_rows = 0
            
        coldelt = res_cols-(Ncols-8)

        if coldelt > 0:
            self.updating_columns = True
            self.values.InsertCols(Ncols, coldelt)
            self.updating_columns = False
            
        elif coldelt < 0:
            self.updating_columns = True
            self.values.DeleteCols(Ncols+coldelt, abs(coldelt))
            self.updating_columns = False
            
        for resR in range(0, res_rows):
            for colR in range(0, res_cols):
                val = "%g" % round(self.Result[resR, colR], 2)
                self.values.SetCellValue(resR, colR+8, val)

        for colup in range(0, res_cols):
            colupdate = colup + 8
            name = u'\u03A0%g' % (colup + 1)
            self.values.SetColLabelValue(colupdate, name)
            for rowupdate in range(0, Nrows):
                col = (255, 130, 0)
                self.values.SetCellBackgroundColour(rowupdate, colupdate, col)
        self.updating_columns = True        
        self.values.AutoSizeColumns() 
        self.updating_columns = False
        
    def permute(self, event):
        res_shape =  self.Result.shape
        if res_shape[1] > 1:
            new_group = np.zeros([res_shape[0],1])
            for iter_r in range(0,res_shape[1]):
                rand = np.random.randint(-1,2)
                new = np.matrix(self.Result[:,iter_r]).T
                new_group += rand*new
                self.Permute_Result = np.hstack((self.Permute_Result,new_group))
            self.Permute_Result = DataFrame(self.Permute_Result.T).drop_duplicates().values.T
            self.Permute_Result = self.Permute_Result.T[self.Permute_Result.T.any(1)].T
            
            perm_shape = self.Permute_Result.shape
            
            Nrows = self.values.GetNumberRows()
            Ncols = self.values.GetNumberCols()           
            
            delt = perm_shape[1] -  (Ncols - res_shape[1] - 8)
            
            if delt > 0:
                self.updating_columns = True
                self.values.InsertCols(Ncols, delt)
                self.updating_columns = False 
                
                for colup in range(0, perm_shape[1]):
                    colupdate = colup + 8 + res_shape[1]
                    name = u'perm \u03A0%g' % (colup + 1 + res_shape[1])
                    self.values.SetColLabelValue(colupdate, name)
                    for rowupdate in range(0, Nrows):
                        col = (70, 140, 255)
                        self.values.SetCellBackgroundColour(rowupdate, colupdate, col)
                        
                        
                for res_permR in range(0, perm_shape[0]):
                    for col_permR in range(0, perm_shape[1]):
                        val = "%g" % round(self.Permute_Result[res_permR, col_permR], 2)
                        self.values.SetCellValue(res_permR, col_permR+8+res_shape[1], val)
        self.updating_columns = True        
        self.values.AutoSizeColumns() 
        self.updating_columns = False
                       
    def reset(self, event):
        Nrows = self.values.GetNumberRows()
        Ncols = self.values.GetNumberCols()
        self.input_mat = []
        self.input_fixed = []
        self.Result = []
        self.Permute_Result = []
        if Nrows > 1 :
            self.updating_columns = True
            self.values.DeleteRows(0,Nrows-1)
            self.updating_columns = False
        if  Ncols > 8:
            self.updating_columns = True
            self.values.DeleteCols(8,Ncols-8)
            self.updating_columns = False
            
    def quit(self, event):
        self.Close()

if __name__ == "__main__":
    app = wx.App()
    frame = Pi_interface(None, -1, 'PI Finder GUI').Show()
    app.MainLoop()