try:
        import wx
        import wx.grid as gridlib
except ImportError:
    raise ImportError,"wxpython module required!"

class Pi_interface(wx.Frame):
    def __init__(self,parent,id,title):
        wx.Frame.__init__(self,parent,id,title,size=(750,600))
        self.parent = parent
        self.initialize()
        
        

    def initialize(self):
                
        panel = wx.Panel(self,-1,(10,20),style=wx.SUNKEN_BORDER)
 
        ColLabels = ["Name","L","T","M",u"\u03F4","N","I","J","","Pi1","Pi2"]
        
        sizer = wx.BoxSizer(wx.VERTICAL)
 
        self.values = gridlib.Grid(panel)
        self.values.CreateGrid(11, 11)
        
        
        for column in range(11):
            
            self.values.SetColLabelValue(column, ColLabels[column])
            self.values.AutoSizeColumns()    
        
        sizer.Add(self.values, 1, wx.EXPAND)
        panel.SetSizerAndFit(sizer)  
        self.SetAutoLayout(True)
        self.SetSizer(sizer)
        

        self.values.Bind(gridlib.EVT_GRID_CELL_CHANGE, self.OnCellChange,) #<---I cannot Get this to work 
        

         
    def OnCellChange(self, event):
        print self.values.GetCellValue(event.GetRow(), event.GetCol()) #<-- so that I can simply retrieve the typed cell value
        
            
if __name__ == "__main__":
    app = wx.App()
    frame = Pi_interface(None,-1,'PI Finder GUI').Show()
    app.MainLoop()
