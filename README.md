# filesynchronization
Folders synchronization program with Tk GUI interface: allow user to select “left” and “right” folders, compare theirs contain, and make synchronization in direction left TO right with 2 options: update and mirror

### Prerequisites
* python3
* Tkinter lib

Install Tkinter for python 3.5 for Windows OS:
```
Tkinter (and, since Python 3.1, ttk) are included with all standard Python distributions
```
Install Tkinter for python 3.5 for Linux OS:
```
sudo apt-get install python3.5-tk
```
## Deployment
Select "left" and "right" folders to compare theirs contain. Comparison is made for each file and nested folders. After comparing you can choose synchronization option through top menu or button on the left bottom corner:
* Update - update right folder with changes and new objects from left directory
* Mirror - make right folder the same as left one    

If you need to compare more folders, you can click on "+" button and add path to additional folder.  
If you need compare folder regularly, you can save session and load it through top menu.
