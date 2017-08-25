# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 17:09:21 2016

@author: IukhymchukS
"""
print('PP4E scrolledtext')
from tkinter import *

class ScrolledText(Frame):
    def __init__(self,parent=None,text='',file=None,width=5,height=16):
        Frame.__init__(self,parent)
        self.pack(expand=YES, fill=BOTH)
        self.makewidget(width,height)
        self.settext(text,file)
        
    def makewidget(self,width,height):
        sbar=Scrollbar(self)
        text=Text(self,relief=SUNKEN,width=width, height=height)
        sbar.pack(side=RIGHT,fill=Y)
        text.pack(expand=YES,fill=BOTH)
        sbar.config(comman=text.yview)
        text.config(yscrollcommand=sbar.set)
        self.text=text
        
    def settext(self,text='',file=None):
        if file:
            text=open(file,'r').read()
        self.text.delete('1.0',END)
        self.text.insert('1.0',text)
        self.text.focus()
        
    def gettext(self):
        return self.text.get('1.0',END+'-1c')
        
if __name__ == '__main__':
    root = Tk()
    if len(sys.argv) > 1:
        st = ScrolledText(file=sys.argv[1]) # filename on cmdline
    else:
        st = ScrolledText(text='Words\ngo here') # or not: two lines
    def show(event):
        print(repr(st.gettext())) # show as raw string
    root.bind('<Key-Escape>', show) # esc = dump text
    root.mainloop()
        