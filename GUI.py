try:
        import wx
        import wx.grid as gridlib
except ImportError:
    raise ImportError("wxpython module required!")
try:
        import svd_PI_finder as PI
except ImportError:
    raise ImportError("PI_Finder module required!")

import numpy as np


class Pi_interface(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(800, 700))
        self.parent = parent
        self.updating_columns = False
        self.initialize()
        self.Result = None

    def initialize(self):

        panel = wx.Panel(self, 1, (10, 20), style=wx.SUNKEN_BORDER)
        self.Button = wx.Button(panel,-1,"Permute Pi Groups", (495,300))  

        ColLabels = ["Name", "L", "T", "M", u"\u03F4", "N", "I", "J"]

        Ncols = len(ColLabels)
        Nrows_initial = 1

        self.values = gridlib.Grid(panel)
        self.values.CreateGrid(Nrows_initial, Ncols)
        self.values.SetSize((600, 300))

        self.values.Bind(gridlib.EVT_GRID_CELL_CHANGE, self.OnCellChange,)
        self.Button.Bind(wx.EVT_BUTTON, self.permute)

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
                if val != '':
                    self.input_mat[update_col-1,update_row] = val            
        if Nrows > 1:
            self.result_input = self.input_mat[self.input_mat.any(1)].T
            self.Result = PI.buck(self.result_input)
        
        
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
                col = (255, 128, 0)
                self.values.SetCellBackgroundColour(rowupdate, colupdate, col)

    def permute(self, event):
        print "Permute!!"

if __name__ == "__main__":
    app = wx.App()
    frame = Pi_interface(None, -1, 'PI Finder GUI').Show()
    app.MainLoop()