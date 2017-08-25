# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 17:02:37 2016

@author: IukhymchukS
"""
from guitools.fsyntool import MakeGui, InputRow
import os
from tkinter import messagebox
from tkinter.messagebox import *
from filesynch.filesync import comparedirs, filesync, copytree, removeDirectory
from pprint import pprint
from tkinter import *
            
class Controller(MakeGui, InputRow):

    def __init__(self):
        MakeGui.__init__(self)

    def start(self):
        self.menuBar = [('File', 0, [('Import session', 0, self.onLoad), ('Save session', 0, self.onSave), ('Quit', 0, self.quit)]),
                        ('Action', 0, [('Compare', 0, self.compare), ('Synch', 0, [('Mirror', 0, self.mirror), ('Update', 0, self.update)])]),
                        ]
        self.toolBar = [('Compare', self.compare, LEFT),('Synch', self.listOption, LEFT),('Quit', self.quit, RIGHT),('Clear', self.clear, RIGHT)]
        self.toolOpt = [('Mirror', self.mirror), ('Update', self.update)]

    def compare(self):
        """
        Core method for comparing "left" and "right" directories. Use widget variables for getting directory names and
        functions from filesync module.
        :return: The results of comparison are recorded to lists: diffs - difference between directories, 
        unique1 - unique objects for left directories, unique2 - unique objects for right directories
        """
        leftone = InputRow.leftval
        rightone = InputRow.rightval
        self.diffs, self.unique1, self.unique2 = [], [], []
        for i in range(len(leftone)):
            if not leftone[i].get() or not rightone[i].get():
                messagebox.showinfo(title='Directory emty', message='Input, please, directories for comparing')
        for i in range(len(leftone)):
            diffs, unique1, unique2 = [], [], []
            left, right=leftone[i].get(),rightone[i].get()
            try:
                assert os.path.exists(left) and os.path.exists(right)
            except AssertionError:
                messagebox.showerror('Path error', 'Bad path directory')
                break
            else:
                diffs, unique1, unique2 = comparedirs(left, right, diffs, unique1, unique2)
                self.diffs.append(diffs)
                self.unique1.append(unique1)
                self.unique2.append(unique2)
                print('Following items differ for folders:')
                pprint(self.diffs)
                print('Following items are unique for left folder:')
                pprint(self.unique1)
                print('Following items are unique for right folder:')
                pprint(self.unique2)
        self.updateLists()

    def updateLists(self):  # Update scrolled text widgets after performing synch operation

        def empty_tree(input_list):
            """Recursively iterate through values in nested lists."""
            for item in input_list:
                if not isinstance(item, list) or not empty_tree(item):
                    return False
            return True

        self.lefttext.delete('1.0', END)
        self.righttext.delete('1.0', END)
        try:  # Handle Exception for case of bad directories during comparing
            for i in range(len(InputRow.leftval)):
                if self.diffs[i]:
                    leftdir = os.path.dirname(self.diffs[i][0][0])
                    rightdir = self.diffs[i][0][1]
                    self.lefttext.insert('end','Following items differ for ' + str(leftdir) + ':\n')
                    self.righttext.insert('end','Following items differ for ' + str(rightdir) + ':\n')
                    for (item, dir2) in self.diffs[i]:
                        fname = os.path.relpath(item, start=leftdir)
                        dstfname = os.path.split(item)[1]
                        dst = os.path.join(dir2, dstfname)
                        self.lefttext.insert('end','   ' + str(fname) + '  ' + str(os.path.getsize(item)) + 'B' + '\n')
                        self.righttext.insert('end','   ' + str(os.path.basename(dst)) + '  ' + str(os.path.getsize(dst)) + 'B' + '\n')

            for i in range(len(InputRow.leftval)):
                if self.unique1[i] or self.unique2[i]:
                    if self.unique1[i]:
                        leftdir = os.path.dirname(self.unique1[i][0][0])
                        rightdir = self.unique1[i][0][1]
                        self.lefttext.insert('end','Following items are unique for ' + str(leftdir) + ':\n')
                        self.righttext.insert('end','Following items are unique for ' + str(rightdir) +':\n')
                        for (fname,dir2) in self.unique1[i]:
                            self.lefttext.insert('end', '   ' + str(os.path.relpath(fname, start=leftdir)) + '\n')
                            self.righttext.insert('end', '\n')
                    else:
                        rightdir = os.path.dirname(self.unique2[i][0][0])
                        leftdir = self.unique2[i][0][1]
                        self.righttext.insert('end','Following items are unique for ' + str(rightdir) + ':\n')
                        self.lefttext.insert('end','Following items are unique for ' + str(leftdir) + ':\n')
                        for (fname,dir1) in self.unique2[i]:
                            self.righttext.insert('end','   ' + str(os.path.relpath(fname, start=rightdir))+'\n')
                            self.lefttext.insert('end','\n')

            if empty_tree(self.diffs) and empty_tree(self.unique1) and empty_tree(self.unique2):
                self.lefttext.insert('end', 'Folders are identical')
                self.righttext.insert('end', 'Folders are identical')
            messagebox.showinfo('Task status', 'Task completed')
        except IndexError:
            print('There is error in directory path')

    def clear(self):
        self.destroy()
        self.__init__()
        pass

    def update(self):  # Update operation log widget
        leftone = InputRow.leftval
        for i in range(len(leftone)):
            filesync(self.diffs[i])
            for(item,dir2) in self.diffs[i]:
                fname = os.path.split(item)[1]
                self.operations.insert('end', 'sync %s - > %s\n' %(str(item),str(os.path.join(dir2,fname))))
                self.operations.see('end')
                self.updateText(fname)
            for item in self.unique1[i]:
                if item[0]:
                    self.operations.insert('end', 'copying %s - > %s\n' %(str(item[0]),str(item[1])))
                    self.operations.see('end')
                    copytree(item[0],item[1])
                    self.updateText(os.path.split(item[0])[1])

    def mirror(self):
        self.update()
        leftone=InputRow.leftval
        for i in range(len(leftone)):
            if self.unique2[i]:
                for item in self.unique2[i]:
                    self.operations.insert('end', 'removing %s \n' % item[0])
                    self.operations.see('end')
                    self.updateText(os.path.split(item[0])[1], side='right')
                removeDirectory(self.unique2[i])
    
    def updateText(self, fname, side='left'):
        where = self.lefttext.search(str(fname), '1.0', END)
#        self.lefttext.mark_set('found',where)
        self.righttext.tag_configure('redText', foreground='red')
        if side == 'left':
            line = int(where.split('.')[0])
            column = int(where.split('.')[1])
            text = self.lefttext.get('%d.%d' %(line,column),'%d.%d lineend' %(line,column))
            self.righttext.mark_set('insert','%d.%d' %((line,column)))
            self.righttext.delete('insert linestart', 'insert lineend')
            self.righttext.insert('%d.%d' %(line,column), str(text))
            self.righttext.tag_add('redText', 'insert linestart', 'insert lineend')
        else:
            where = self.righttext.search(str(fname),'1.0',END)
            line = int(where.split('.')[0])
            column = int(where.split('.')[1])
            self.righttext.mark_set('found', '%d.%d' %((line, column)))
            self.righttext.delete('found linestart', 'found lineend')

    def listOption(self):
        win=Toplevel(relief=FLAT)    
        lb=Listbox(win)
        lb.pack(side=TOP, fill=BOTH, expand=YES)
        for (label, com) in self.toolOpt:
            lb.insert(END,label)
        Button(win, text='Ok', command=lambda: self.fetchCommand(win,lb)).pack(side=BOTTOM)
        
    def fetchCommand(self,win,lb):
        lab=lb.get(ACTIVE)
        for (label,com) in self.toolOpt:
            if label==lab:
                com()
        win.destroy()

if __name__=='__main__':
    Controller().mainloop()
