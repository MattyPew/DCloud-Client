from tkinter import *
import os
import ctypes
import webbrowser
import easygui
import json
from tinydb import TinyDB, Query
import os
db = TinyDB('db.json')
global actual_directory
actual_directory = "/."
query = Query()
def cls():
    os.system("cls")





##########################################################################################
#                                       DIRECTORY                                        #
##########################################################################################
def list_dir():
    print("Directory: "+actual_directory)
    results = db.search(query.directory == actual_directory) # returns a list
    list = []
    for res in results:
        list.append(res["item_name"])
    return list
def mk_dir(folder_name=str):
    db.insert({'directory': actual_directory, "type": "folder", "item_name": folder_name})
##########################################################################################



def openWebsite():
    webbrowser.open("https://github.com/MattyPew/DCloud-Client/tree/main")


# TKINTER CODE

# Increase Dots Per inch so it looks sharper
ctypes.windll.shcore.SetProcessDpiAwareness(True)

root = Tk()
# set a title for our file explorer main window
root.title('DCloud Client')
root.geometry("750x500")

root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(1, weight=1)

def TKpathChange(*event):
    global actual_directory
    # Get all Files and Folders from the given Directory
    directory = list_dir()
    # Clearing the list
    list.delete(0, END)
    # Inserting the files and directories into the list
    for file in directory:
        list.insert(0, file)
    entry.config(state="normal")
    entry.delete(0, END)
    entry.insert(0, actual_directory)
    entry.config(state= "disabled")


def TKchangePathByClick(event=None):
    global actual_directory
    # Get clicked item.
    picked = list.get(list.curselection()[0])
    # get the complete path by joining the current path with the picked item
    # Check if item is file, then open it
    picked = db.search((query.item_name == picked) & (query.directory == actual_directory))
    picked = picked[0]
    if picked["type"] == "folder":
        actual_directory = actual_directory+"/"+picked["item_name"]
        print(actual_directory)
        TKpathChange()
    elif picked["type"] == "file":
        # Open file script goes there
        pass
    else:
        print("Error")


def TKgoBack(event=None):
    global actual_directory
    if not actual_directory == "/.":
        splited_dir = actual_directory.split("/")
        new_dir = ""
        index = len(splited_dir)
        print(index)
        for folder in splited_dir:
            index = index-1
            if index > 0:
                new_dir = new_dir+"/"+folder
        new_dir = new_dir[1:]
        actual_directory = new_dir
        print(actual_directory)
        TKpathChange()
    else:
        print("Already on top!")


def TKnewFolderOpen_popup():
    global top
    top = Toplevel(root)
    top.geometry("250x150")
    top.resizable(False, False)
    top.title("Create folder")
    top.columnconfigure(0, weight=1)
    Label(top, text='Enter Folder name').grid()
    Entry(top, textvariable=newFolderName).grid(column=0, pady=10, sticky='NSEW')
    Button(top, text="Create", command=TKnewFolder).grid(pady=10, sticky='NSEW')

def TKnewFolder():
    if len(newFolderName.get().split('.')) != 1:
        print("Forbiden character!")
    else:
        if newFolderName.get() in list_dir():
            print("Already exist!")
        else:
            mk_dir(newFolderName.get())
            top.destroy()
            TKpathChange()
    # destroy the top


def TKremoveFolder():
    picked = list.get(list.curselection()[0])
    picked = db.search((query.item_name == picked) & (query.directory == actual_directory))
    picked = picked[0]
    db.remove((query.item_name == picked["item_name"]) & (query.directory == actual_directory))
    TKpathChange()

def importFilePopup():
    file = easygui.fileopenbox(msg="Select import file (.dcloudfile).",default="*.dcloudfile",filetypes=['*.dcloudfile'])
    with open(file, 'r') as f:
        data = json.load(f)
        f.close()
    if data["item_name"] in list_dir():
        print("Already exist!")
    else:
        db.insert({'directory': actual_directory, "type": "file", "item_name": data["item_name"], "links": data["links"], "key": data["key"], "size": data["size"], "description": data["description"]})
    TKpathChange()
top = ''

def exportFilePopup():
    picked = list.get(list.curselection()[0])
    picked = db.search((query.item_name == picked) & (query.directory == actual_directory))
    picked = picked[0]
    if picked["type"] == "file":
        name = picked["item_name"]+".dcloudfile"
        saveTo = easygui.filesavebox(msg="Select export location (.dcloudfile).",default=name,filetypes=['*.dcloudfile'])
        data = {"item_name": picked["item_name"], "links": picked["links"], "key": picked["key"], "size": picked["size"], "description": picked["description"]}
        with open(saveTo, "w") as f:
            f.write((str(data)).replace("'",'"'))
            f.close()
        print("Done")
    else:
        print("Not file!")

def TKshowFileDescriptionPopup():
    picked = list.get(list.curselection()[0])
    picked = db.search((query.item_name == picked) & (query.directory == actual_directory))
    picked = picked[0]
    if picked["type"] == "file":
        global top
        top = Toplevel(root)
        top.geometry("500x750")
        top.resizable(False, False)
        top.title("File description")
        top.columnconfigure(0, weight=1)
        Label(top, text=("Name: "+picked["item_name"])).grid()
        Label(top, text=("Size: "+picked["size"])).grid()
        Label(top, text=("Description: "+picked["description"])).grid()
        Label(top, text=("Key: "+picked["key"])).grid()

    else:
        print("Not file!")


# String variables
newFolderName = StringVar(root, "NewFolder", 'new_name')


Button(root, text='Folder Up', command=TKgoBack).grid(
    sticky='NSEW', column=0, row=0
)
#Button(root, text="TEMP", command=exit).grid(sticky="NSEW", column=0, row=1)

# Keyboard shortcut for going up
root.bind("<Alt-Up>", TKgoBack)


entry = Entry(root, text="")
entry.grid(sticky='NSEW', column=1, row=0, ipady=10, ipadx=10)

# List of files and folder
list = Listbox(root)
list.grid(sticky='NSEW', column=1, row=1, ipady=10, ipadx=10)

# List Accelerators
list.bind('<Double-1>', TKchangePathByClick)
list.bind('<Return>', TKchangePathByClick)

def donothing():
    pass
# Menu
menubar = Menu(root)
# ADVANCED in MENU BAR
advancedmenu = Menu(menubar, tearoff=0)
advancedmenu.add_command(label="About", command=openWebsite)
advancedmenu.add_separator()
advancedmenu.add_command(label="Quit", command=root.quit)
menubar.add_cascade(label="Advanced", menu=advancedmenu)

# FILE/FOLDER in MENU BAR
basicmenu = Menu(menubar, tearoff=0)
basicmenu.add_command(label="Create Folder", command=TKnewFolderOpen_popup)
basicmenu.add_command(label="Import File", command=importFilePopup)
basicmenu.add_command(label="Export File", command=exportFilePopup)
basicmenu.add_command(label="Description", command=TKshowFileDescriptionPopup)
basicmenu.add_command(label="Delete", command=TKremoveFolder)
menubar.add_cascade(label="File/Folder", menu=basicmenu)

# IMPORT in MENU BAR
importmenu = Menu(menubar, tearoff=0)
importmenu.add_command(label="Upload File")
menubar.add_cascade(label="Upload", menu=importmenu)



# CREATE MENUBAR
root.config(menu=menubar)

# Call the function so the list displays
TKpathChange('')
# run the main program
root.mainloop()
