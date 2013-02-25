try:
        import wx
        import wx.grid as gridlib
except ImportError:
    raise ImportError,"wxpython module required!"
try:
        import PI_Finder as PI
except ImportError:
    raise ImportError,"PI_Finder module required!"
    
import numpy as np

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
 
        self.input_mat = np.array([[0,0,0,0,0,0,0]])
         
    def OnCellChange(self, event):
        row = self.values.GetNumberRows()        
       
        [m_row, m_col] = self.input_mat.shape
        delt = row - m_row
                
        if delt > 0:
            add_row = np.array([[0,0,0,0,0,0,0]])
            for r_add in range(delt):
                self.input_mat = np.vstack((self.input_mat,add_row))    
        if delt < 0:
            self.input_mat = self.input_mat[:+delt,:]
    
        for update_col in range(1,7):
            for update_row in range(0,row):
                val = self.values.GetCellValue(update_row, update_col)
                if val == '':
                    self.input_mat[update_row,update_col] = 0
                else:
                    self.input_mat[update_row,update_col-1] = val 
        
        print PI.buck(self.input_mat)
       
        
        
if __name__ == "__main__":
    app = wx.App()
    frame = Pi_interface(None,-1,'PI Finder GUI').Show()
    app.MainLoop()
