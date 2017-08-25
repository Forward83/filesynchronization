# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 17:45:24 2016

@author: IukhymchukS
"""

import os, sys, shutil, pprint
blocksize=1024*1000
from queue import Queue
def getatt(blocksize):
    if len(sys.argv)==2 and sys.argv[1]=='-help':
        print ('Directory synchronization script. Use filesync.py [srcdir  dstdir] (blocksize=1024000B). Use "chcp 1251" command to change encoding')
        return None
    elif len(sys.argv)==4:
        dir1=sys.argv[1]
        dir2=sys.argv[2]
        blocksize=sys.argv[3]
    else:
        dir1=sys.argv[1]
        dir2=sys.argv[2]
        blocksize=blocksize
    return dir1,dir2,blocksize
    
def difference(seq1,seq2):
    return [item for item in seq1 if item not in seq2]

def intersect(seq1,seq2):
    return [item for item in seq1 if item in seq2]
 
def comparefiles(file1,file2,blocksize=blocksize):
    fh1=open(file1,'rb')
    fh2=open(file2,'rb')
    data1=fh1.read(blocksize)
    data2=fh2.read(blocksize)
    try:
        while data1 and data2:
            if data1!=data2:
                return False
                break
            data1=fh1.read(blocksize)
            data2=fh2.read(blocksize)
    except EOFError:
        print('Some file is ended')
    fh1.close()
    fh2.close()
    return True
    
def comparedirs(dir1,dir2,diffs,unique1,unique2):
    names1=os.listdir(dir1)
    names2=os.listdir(dir2)
    common=intersect(names1,names2)
    missed=common[:]
    nameuniq1=difference(names1,names2)
    nameuniq2=difference(names2,names1)
    for item in nameuniq1:                                      #recording unique files and folder 
        fullpath=os.path.join(dir1,item)
        unique1.append((fullpath,dir2))
    for item in nameuniq2:                                      #recording unique files and folder 
        fullpath=os.path.join(dir2,item)
        unique2.append((fullpath,dir1))
    for name in common:                                         #Comparing files
        path1=os.path.join(dir1,name)
        path2=os.path.join(dir2,name)
        if os.path.isfile(path1) and os.path.isfile(path2):
            try:
                print ('comparing files:', repr(path1),' -> ',repr(path2))
            except UnicodeEncodeError:
                pass
#            print('putting to the queue')
#            queue.put('comparing files: %s - > %s\n' % (str(path1),str(path2)),timeout=0.05,block=True)
#            queue.put_nowait('comparing files: %s - > %s\n' % (str(path1),str(path2)))
            eq=comparefiles(path1,path2)
            if not eq:
                diffs.append((path1,dir2))
            missed.remove(name)
            
    for name in common:                                         #comparing directories
        path1=os.path.join(dir1,name)
        path2=os.path.join(dir2,name)
        if os.path.isdir(path1) and os.path.isdir(path2):
            missed.remove(name)
            comparedirs(path1,path2,diffs,unique1,unique2)
    return (diffs,unique1,unique2)
    
def filesync(diffs):
    for (item,dir2) in diffs:
        fname=item.split('\\')[-1]
        dst=os.path.join(dir2,fname)
#        queue.put('copying %s - > %s' % (str(item),str(dst)))
        shutil.copy(item,dst)
    return 'Files sync is completed'

def copytree(src, dst, symlinks=False, ignore=None):
#    print(src,dst)
    if os.path.isfile(src):
        shutil.copy(src,dst)
    else:
        dstFold=src.split('\\')[-1]
        d=os.path.join(dst,dstFold)
        shutil.copytree(src,d)
        
def removeDirectory(unique2):
    for (item,dir1) in unique2:
        if os.path.isdir(item):
            shutil.rmtree(item,ignore_errors=False)
        else:
            os.remove(item)
    return "Removing files, directories from %s" % item
    
if __name__=='__main__':
    unique1=[]
    unique2=[]
    diffs=[]
    attuple=getatt(blocksize)
    if attuple is None:
        pass
    else:
        (r1,r2,r3)=comparedirs(attuple[0],attuple[1],diffs,unique1,unique2)
        print('Following files differs:')
        pprint.pprint(r1)
        print('Following items are unique for',attuple[0],':')
        pprint.pprint(r2)
        print('Following items are unique for ',attuple[1],': ')
        pprint.pprint(r3)
        if input('Would you like to sync files and directories? ') in ('Y','y','yes','Yes','YES'):
            if r1:
                filesync(r1)
            if r2:
                for item in r2:
                    copytree(item[0],item[1])
            if r3:
                removeDirectory(r3)
        print('Folder sync is completed')



        
            
    
            
        

