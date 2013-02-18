import Tkinter
from Tkinter import *
import xlrd
import numpy as np

power_array = np.zeros([7,1])


class Main_window(Frame):
    
    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")
            
        self.parent = parent
            
        self.initUI()
            
    def initUI(self):
        
        self.parent.title("Buckingham Pi")
        self.pack(fill=BOTH, expand=1)
        
        self.edit_window = Canvas(self, width=690, height=350)         
     
        self.edit_window.pack()       
        self.edit_window.place(x=30,y=70)
        
        #Number
        Label(self.edit_window,text="Num",bd=1,relief="raised").grid(row=0,column=0,sticky='nswe')
        #Name
        Label(self.edit_window,text="Name",bd=1,relief="raised").grid(row=0,column=1,sticky='nswe')
        #Length
        Label(self.edit_window,text="L",bd=1,relief="raised").grid(row=0,column=2,sticky='nswe')
        #Time
        Label(self.edit_window,text="T",bd=1,relief="raised").grid(row=0,column=3,sticky='nswe')
        #Mass
        Label(self.edit_window,text="M",bd=1,relief="raised").grid(row=0,column=4,sticky='nswe')
        #Temperature
        Label(self.edit_window,text=u"\u03F4",bd=1,relief="raised").grid(row=0,column=5,sticky='nswe')
        #Quantity
        Label(self.edit_window,text="N",bd=1,relief="raised").grid(row=0,column=6,sticky='nswe')
        #Current
        Label(self.edit_window,text="I",bd=1,relief="raised").grid(row=0,column=7,sticky='nswe')
        #Luminous intensity
        Label(self.edit_window,text="J",bd=1,relief="raised").grid(row=0,column=8,sticky='nswe')
        
        #separation line
        Label(self.edit_window,bd=1).grid(row=0,column=9,sticky='nswe')
        
        for row in range(1,10):
            for col in range(9):
                if col ==0:
                    Label(self.edit_window,text="%d"%(row),bd=1,relief="raised").grid(row=row,column=0,sticky='nswe')
                else:
                    Entry(self.edit_window,bd=1,relief="raised",width=3).grid(row=row,column=col,sticky='nswe')

       ####the problem now arose in finding a way to reliably access the etry cells#### 
        
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
