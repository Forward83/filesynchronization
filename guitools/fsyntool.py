# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 17:04:40 2016
Classes for building GUI part

@author: IukhymchukS
"""
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import askdirectory, asksaveasfile, askopenfile
from tkinter.scrolledtext import ScrolledText
import pickle 

root=Tk()
class MakeGui(Frame):
    """
    The main class for building GUI interface. Uses InputRow class for creating custom q-ty of directories,
    redrawing window during import, clear action 
    """
    menuBar=[]
    toolBar=[]
    def __init__(self, numrows=1, parent=root):
        Frame.__init__(self,parent)
        self.pack(expand=YES, fill=BOTH)
        self.start()  # This method is adapted in the controller class. It initializes top menu items, and toolbar items
        self.makeMenu()
        self.makeToolbar()
        self.makeWidget(numrows)
        
    def makeMenu(self):
        top=Menu(self)
        self.master.config(menu=top)
        for (lab,key,items) in self.menuBar:
            optitem=Menu(top)
            self.addMenuItem(optitem, items)
            top.add_cascade(label=lab, underline=key, menu=optitem)
        
    def addMenuItem(self, top, items):
        for item in items:
            if item=='separator':
                top.add_separator()
            elif type(item) == list:
                for i in item:
                    top.entryconfig(i, state=DISABLED)
            elif type(item[2]) != list:
                top.add_command(label=item[0], underline=item[1], command=item[2])
            else:
                submenu = Menu(top)
                self.addMenuItem(submenu,item[2])
                top.add_cascade(label = item[0], underline=item[1], menu=submenu)
    
    def makeToolbar(self):
        row=Frame(self, pady=2)
        row.pack(side=BOTTOM, fill=X, expand=NO)
        for (lab, cb, where) in self.toolBar:
            Button(row, text=lab, command=cb, padx=5).pack(side=where, expand=NO)
        Label(row,text='Operation logs:',font=('times', 12, 'italic'),padx=1).pack(side=LEFT)
        self.operations = ScrolledText(row, width=50, height=1, padx=10)
        self.operations.pack(side=LEFT, fill=BOTH, expand=YES)
        
    def makeWidget(self,numrows):
        self.addLabel()
        InputRow(numrows,parent=self)
        self.addTextbox()

    def addLabel(self):
        row=Frame(self,pady=2)
        row.pack(side=TOP, expand=NO, fill=X)
        Label(row,text='LEFT DIRECTORY', relief=GROOVE, padx=40).pack(side=LEFT)
        Label(row,text='RIGHT DIRECTORY', relief=GROOVE, padx=40).pack(side=RIGHT)
        
    def addTextbox(self):
        row=Frame(self)
        row.pack(side = BOTTOM, expand=YES, fill=BOTH)
        self.lefttext = ScrolledText(row, width=76)
        self.righttext = ScrolledText(row, width=76)
        self.lefttext.pack(side=LEFT, fill=Y,expand=YES)
        self.righttext.pack(side=RIGHT,fill=Y,expand=YES)
        
class InputRow(Frame):
    leftval=[]  # List of StringVar objects. Used to have access to the values of these objects
    rightval=[]
    def __init__(self, numrows, parent=None, width=60, minus=False):
        """
        :param numrows: Number of instances (rows for entering input directories
        :param parent: parent widget, if you need to place instance to it
        :param width: widget width
        :param minus: include minus button near the widget or no 
        """
        Frame.__init__(self, parent)
        self.pack(expand=NO, fill=X, anchor=N)
        plus = Button(self, text='+')
        plus.pack(side=LEFT)
        if minus:
            Button(self, text='-', command=lambda: self.minusCb(left,right)).pack(side=LEFT)
        left=StringVar()
        right=StringVar()
        ent1 = Entry(self, textvariable=left, width=width).pack(side=LEFT)
        ent2 = Entry(self, textvariable=right, width=60).pack(side=RIGHT)
        Button(self, text='Browse', command=lambda: left.set(left.get() or askdirectory())).pack(side=LEFT)
        Button(self, text='Browse', command=lambda: right.set(right.get() or askdirectory())).pack(side=RIGHT)
        InputRow.leftval.append(left)
        InputRow.rightval.append(right)
        plus.config(command=self.plusCb)
        for i in range(numrows-1):
            self.plusCb()

    def plusCb(self):
        InputRow(1, parent=self.master, width=57, minus=True)

    def minusCb(self, left, right):  # before destroy instance, search var object and remove it from left, right lists
        for item in InputRow.leftval:
            if left.get() == item.get():
                InputRow.leftval.remove(item)
                break
        for item in InputRow.rightval:
            if right.get() == item.get():
                InputRow.rightval.remove(item)
                break
        self.destroy()

    def onSave(self):
        leftdirs = []
        rightdirs = []
        for i in range (len(InputRow.leftval)):
            leftdirs.append(InputRow.leftval[i].get())
            rightdirs.append(InputRow.rightval[i].get())
        fname = asksaveasfile(mode='wb')
        pickle.dump((leftdirs, rightdirs), fname)
        fname.close()

    def onLoad(self):
        InputRow.leftval = []
        InputRow.rightval = []
        fname = askopenfile(mode='rb')
        (leftdirs, rightdirs) = pickle.load(fname)
        count = len(leftdirs)
        MakeGui.destroy(self)
        MakeGui.__init__(self, numrows=count, parent=root)
        self.master.update()
        for i in range(len(leftdirs)):
            InputRow.leftval[i].set(leftdirs[i])
            InputRow.rightval[i].set(rightdirs[i])
            print(leftdirs[i], rightdirs[i])
        
if __name__=='__main__':
    root=Tk()
    MakeGui(parent=root).mainloop()

##################################################################

        
    