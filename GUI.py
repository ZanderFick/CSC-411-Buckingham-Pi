import Tkinter
from Tkinter import *
import xlrd


class Main_window(Frame):
    
    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")
            
        self.parent = parent
            
        self.initUI()
            
    def initUI(self):
        
        self.parent.title("Buckingham Pi")
        self.pack(fill=BOTH, expand=1)
        
        #set up the choice list
        Wb = xlrd.open_workbook("Base Units.xls")
        parameter_sheet = Wb.sheet_by_index(0)
        
        choose_parameter = Listbox(self,bg="grey",selectmode="SINGLE")         
        
        for r in range(parameter_sheet.nrows):
            name = parameter_sheet.cell(r,0).value
            choose_parameter.insert(END,name)
        
        choose_parameter.pack()       
        choose_parameter.place(x=10,y=10)
        
        add_parameter = Button(self, text ="add parameter")
        add_parameter.place(x=10,y= 180)
            
def main():
    
    root = Tk()
    
    w = 750 
    h = 600
    width_pos = (root.winfo_screenwidth()- w)/2
    height_pos = (root.winfo_screenheight()- h)/2
    
    root.geometry('%dx%d+%d+%d'%(w, h, width_pos, height_pos))
    
    app = Main_window(root)
        
    root.mainloop()
    
    
    display = Frame(root)
    

if __name__ == '__main__':
    main()
