import linecache
config_webhook = linecache.getline("webhook.txt",1).rstrip("\n")
if config_webhook == "":
    print("You need to add webhook url into config.py!")
    exit()

from tkinter import *
import os
import ctypes
import webbrowser
import easygui
import json
from tinydb import TinyDB, Query
import os
import hashlib
from filesplit.split import Split
import os
from cryptography.fernet import Fernet
import shutil
import easygui
import requests
from os import listdir
from os.path import isfile, join
from win10toast import ToastNotifier
from filesplit.merge import Merge
toast = ToastNotifier()
default_direcory = os.getcwd()
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
        db.insert({'directory': actual_directory, "type": "file", "item_name": data["item_name"], "links": data["links"], "key": data["key"], "size": data["size"], "description": data["description"], "hash": data["hash"]})
    TKpathChange()
top = ''

def exportFilePopup():
    picked = list.get(list.curselection()[0])
    picked = db.search((query.item_name == picked) & (query.directory == actual_directory))
    picked = picked[0]
    if picked["type"] == "file":
        name = picked["item_name"]+".dcloudfile"
        saveTo = easygui.filesavebox(msg="Select export location (.dcloudfile).",default=name,filetypes=['*.dcloudfile'])
        data = {"item_name": picked["item_name"], "links": picked["links"], "key": picked["key"], "size": picked["size"], "description": picked["description"], "hash": picked["hash"]}
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
        # top.geometry("500x750")
        top.resizable(False, False)
        top.title("File description")
        top.columnconfigure(0, weight=1)

        links_list_formated = "\n"
        for link in picked["links"]:
            links_list_formated = links_list_formated + link+ "\n"


        Label(top, text=("Name: \n"+picked["item_name"])).grid()
        Label(top, text=("Hash (MD5): \n"+picked["hash"])).grid()
        Label(top, text=("Size: \n"+picked["size"])).grid()
        Label(top, text=("Key: \n"+picked["key"])).grid()
        Label(top, text=("Description: \n"+picked["description"])).grid()
        Label(top, text=("Sources: "+links_list_formated)).grid()
        
        

    else:
        print("Not file!")


def upload():
    upload_file_description = DescriptionText.get()
    top.destroy()
    toast.show_toast(
    "DCloud Client",
    "I am uploading your file, do not close DCloud Client! I will show again after uploading is done.",
    duration = 0,
    icon_path = "icon.ico",
    threaded = True,
)


    upload_file_description = DescriptionText.get()
    upload_temp_directory = default_direcory+"\\upload_temp"
    upload_temp_chunks_directory = upload_temp_directory+"\\upload_temp_chunks"
    # Making folders
    os.chdir(default_direcory)
    if os.path.exists(upload_temp_directory) == False:
        os.mkdir(upload_temp_directory)
    else:
        shutil.rmtree(upload_temp_directory)
        os.mkdir(upload_temp_directory)
    if os.path.exists(upload_temp_chunks_directory) == False:
        os.mkdir(upload_temp_chunks_directory)
    else:
        shutil.rmtree(upload_temp_chunks_directory)
        os.mkdir(upload_temp_chunks_directory)

    # Making encrypted copy
    fernet = Fernet(bytes(upload_file_key,'utf-8'))

    with open(upload_file, 'rb') as f:
        original = f.read()

    encrypted = fernet.encrypt(original)
    encrypted_location = upload_temp_directory+"\\"+upload_file_name

    with open(encrypted_location, 'wb') as f_enc:
        f_enc.write(encrypted)

    # Split into chunks
    
    split = Split(inputfile=encrypted_location, outputdir=upload_temp_chunks_directory)
    split.bysize(24999999, False, False, None)

    # Upload
    files_for_upload = [f for f in listdir(upload_temp_chunks_directory) if isfile(join(upload_temp_chunks_directory, f))]
    from discord_webhook import DiscordWebhook

    index = 0
    links_list = []
    os.chdir(upload_temp_chunks_directory)
    while index < len(files_for_upload):
        print(index)
        webhook = DiscordWebhook(url=config_webhook)
        with open(files_for_upload[index], "rb") as f:
            webhook.add_file(file=f.read(), filename=files_for_upload[index])
            f.close()
        response = webhook.execute()
        data_json = response.content.decode("utf-8")

        data = json.loads(data_json)

        data = data["attachments"]
        data = data[0]
        link = data["url"]

        links_list.append(link)
        index = index+1
    upload_file_source = links_list
    db.insert({'directory': actual_directory, "type": "file", "item_name": upload_file_name, "links": upload_file_source, "key": upload_file_key, "size": upload_file_size, "description": upload_file_description, "hash": upload_file_hash})
    TKpathChange()
    os.chdir(default_direcory)
    if os.path.exists(upload_temp_directory) == True:
        shutil.rmtree(upload_temp_directory)
    if os.path.exists(upload_temp_chunks_directory) == True:
        shutil.rmtree(upload_temp_chunks_directory)
    toast.show_toast(
    "DCloud Client",
    "I sucessfully uploaded your file, you can close DCloud Client now! ",
    duration = 0,
    icon_path = "icon.ico",
    threaded = True,
)
    



def UploadPopup():
    global upload_file
    global upload_file_hash
    global upload_file_key
    global upload_file_name
    global upload_file_size

    upload_file = easygui.fileopenbox(msg="Select file to be uploaded: ")

    # Get file name
    upload_file_name = os.path.basename(upload_file)

    # Get file hash
    with open(upload_file, 'rb') as f:
        f_contents = f.read()
        f.close()
    upload_file_hash = hashlib.md5(f_contents).hexdigest()

    # Get file size
    upload_file_size = str(os.path.getsize(upload_file))

    # Get encryption key
    upload_file_key = Fernet.generate_key().decode("utf-8") 

    global top
    top = Toplevel(root)
    # top.geometry("500x750")
    top.resizable(False, False)
    top.title("Confirm Upload")
    top.columnconfigure(0, weight=1)

    Label(top, text=("Name: \n"+upload_file_name)).grid()
    Label(top, text=("Hash (MD5): \n"+upload_file_hash)).grid()
    Label(top, text=("Size: \n"+upload_file_size)).grid()
    Label(top, text=("Key: \n"+upload_file_key)).grid()
    Label(top, text="Description: ").grid()
    Entry(top, textvariable=DescriptionText).grid()
    Button(top, text="Continue", command=upload).grid()

def download():
    os.chdir(default_direcory)
    top.destroy()
    toast.show_toast(
    "DCloud Client",
    "I am downloading your file, do not close DCloud Client! I will show again after downloading is done.",
    duration = 0,
    icon_path = "icon.ico",
    threaded = True,
    )
    #metadata_file_download[]
    download_temp_directory = default_direcory+"\\download_temp"
    download_temp_chunks_directory = download_temp_directory+"\\download_temp_chunks"
    # Making folders
    os.chdir(default_direcory)
    if os.path.exists(download_temp_directory) == False:
        os.mkdir(download_temp_directory)
    else:
        shutil.rmtree(download_temp_directory)
        os.mkdir(download_temp_directory)
    if os.path.exists(download_temp_chunks_directory) == False:
        os.mkdir(download_temp_chunks_directory)
    else:
        shutil.rmtree(download_temp_chunks_directory)
        os.mkdir(download_temp_chunks_directory)

    os.chdir(download_temp_chunks_directory)
    for url in metadata_file_download["links"]:
        f_url = requests.get(url, allow_redirects=True)
        f_name = f_url.headers.get('content-disposition').replace("attachment; filename=","")
        print("Downloading: "+f_name)
        with open(f_name, 'wb') as f:
            f.write(f_url.content)
            f.close()

    merge = Merge(download_temp_chunks_directory, download_temp_directory, metadata_file_download["item_name"])
    merge.merge(True, False)
    fernet = Fernet(bytes(metadata_file_download["key"], 'UTF-8'))
    os.chdir(download_temp_directory)
    with open(metadata_file_download["item_name"], 'rb') as enc_file:
        encrypted = enc_file.read()
        enc_file.close()
    decrypted = fernet.decrypt(encrypted)
    with open(saveDownload, 'wb') as dec_file:
        dec_file.write(decrypted)
        dec_file.close()

    with open(saveDownload, "rb") as f:
        downloaded_file_hash = hashlib.md5(f.read()).hexdigest()
        f.close()
        

    if downloaded_file_hash == metadata_file_download["hash"]:
        print("Hashes match!")
        toast.show_toast(
        "DCloud Client",
        "I sucessfully downloaded your file, you can close DCloud Client now! ",
        duration = 0,
        icon_path = "icon.ico",
        threaded = True,
        )
    else:
        print("Hashes dont match!")
        print("Cloud hash: "+str(metadata_file_download["hash"]))
        print("Donwloaded hash: "+str(downloaded_file_hash))
        toast.show_toast(
        "DCloud Client",
        "File is downloaded but hashes didnt matched, you can close DCloud Client now! ",
        duration = 0,
        icon_path = "icon.ico",
        threaded = True,
        )
    os.chdir(default_direcory)
    if os.path.exists(download_temp_directory) == True:
        shutil.rmtree(download_temp_directory)
    if os.path.exists(download_temp_chunks_directory) == True:
        shutil.rmtree(download_temp_chunks_directory)

def DownloadPopup():
    global saveDownload
    global metadata_file_download
    
    picked = list.get(list.curselection()[0])
    picked = db.search((query.item_name == picked) & (query.directory == actual_directory))
    picked = picked[0]
    saveDownload = easygui.filesavebox("Select download directory:", default=picked["item_name"])
    metadata_file_download = picked
    if picked["type"] != "folder":
        global top
        top = Toplevel(root)
        # top.geometry("500x750")
        top.resizable(False, False)
        top.title("Confirm Download")
        top.columnconfigure(0, weight=1)

        formated_source_text = ""
        for link in picked["links"]:
            formated_source_text = formated_source_text + "\n" + link
        Label(top, text=("Download into: \n"+saveDownload)).grid
        Label(top, text=("Name: \n"+picked["item_name"])).grid()
        Label(top, text=("Hash (MD5): \n"+picked["hash"])).grid()
        Label(top, text=("Size: \n"+picked["size"])).grid()
        Label(top, text=("Key: \n"+picked["key"])).grid()
        Label(top, text="Description: \n"+picked["description"]).grid()
        Label(top, text="Source: "+formated_source_text).grid()
        Button(top, text="Continue", command=download).grid()



# String variables
newFolderName = StringVar(root, "NewFolder", 'new_name')
DescriptionText = StringVar(root, "Empty description", "new_name")


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
importmenu.add_command(label="Upload File", command=UploadPopup)
importmenu.add_command(label="Download File", command=DownloadPopup)
menubar.add_cascade(label="Upload/Download", menu=importmenu)



# CREATE MENUBAR
root.config(menu=menubar)

# Call the function so the list displays
TKpathChange('')
# run the main program
root.mainloop()

#Lets gooo 500