try:
        import wx
        import wx.grid as gridlib
except ImportError:
    raise ImportError,"wxpython module required!"
import numpy as np

input_mat = np.array([[]])

class Pi_interface(wx.Frame):
    def __init__(self,parent,id,title):
        wx.Frame.__init__(self,parent,id,title,size=(800,700))
        self.parent = parent
        self.initialize()                

    def initialize(self):
                
        panel = wx.Panel(self,-1,(10,20),style=wx.SUNKEN_BORDER)
 
        ColLabels = ["Name","L","T","M",u"\u03F4","N","I","J"," ","Pi1","Pi2"]
        
        sizer = wx.BoxSizer(wx.VERTICAL)
 
        self.values = gridlib.Grid(panel)
        self.values.CreateGrid(11, 11)
                
        sizer.Add(self.values, 1, wx.EXPAND)
        panel.SetSizerAndFit(sizer)  
        self.SetAutoLayout(True)
        self.SetSizer(sizer)        

        self.values.Bind(gridlib.EVT_GRID_CELL_CHANGE, self.OnCellChange,) 

        [col, row]= [self.values.GetNumberCols(), self.values.GetNumberRows()]
        
        
        for column in range(col):
            
            self.values.SetColLabelValue(column, ColLabels[column])
            self.values.AutoSizeColumns()  
        
        for r in range (0,row):
            for c in range (8,col):            
                self.values.SetReadOnly(r,c)     
                
         
    def OnCellChange(self, event):
        print  self.values.GetCellValue(event.GetRow(), event.GetCol())
        active = event.GetRow(), event.GetCol()
        
        row = self.values.GetNumberRows()
        [m_col, m_row] = input_mat.shape
        delt = row - m_row
        print delt
                   # new_row = [0,0,0,0,0,0,0]
           # input_mat = input_mat.concatenate(new_row)
    
        
if __name__ == "__main__":
    app = wx.App()
    frame = Pi_interface(None,-1,'PI Finder GUI').Show()
    app.MainLoop()
