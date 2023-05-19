import os, telegramhelper, discordhelper
import tkinter as tk
from tkinter import messagebox

def left_click(filename):
    root.withdraw()
    print("Left click on file:", filename)
    if filename.endswith(".tidlists"):
        telegramhelper.downloadFile(filename[:-9])
    elif filename.endswith(".linkslists"):
        discordhelper.linkslistsfile_to_file_presplit(filename[:-11])
    else:
        telegramhelper.uploadFile(filename)
    os.remove(filename)
    root.deiconify()
    update_file_index()

def right_click(filename):
    root.withdraw()
    print("Right click on file:", filename)
    if filename.endswith(".tidlists"):
        telegramhelper.downloadFile(filename[:-9])
    elif filename.endswith(".linkslists"):
        discordhelper.downloadFile(filename[:-11])
    else:
        discordhelper.uploadFile(filename)
    os.remove(filename)
    root.deiconify()
    update_file_index()

def update_file_index():
    for widget in root.winfo_children():
        widget.destroy()
    show_files()

def show_files():
    folder = os.getcwd()
    files = os.listdir(folder)

    exclude = ["readme.md", "README.md", ".DS_Store", "LICENSE", ".gitignore"] #You can exclude file here wich below to the bot itself, you dont need to exclude folders or .py files!

    for file in files:
        if os.path.isdir(file) or file in exclude or file.endswith(".py"):
            continue
        else:
            btn = tk.Button(root, text=file, bg="red", command=lambda file=file:left_click(file), width=100, height=2)
            btn.pack(fill="x")
            btn.bind("<Button-2>", lambda event, file=file:right_click(file))

root = tk.Tk()
show_files()
root.mainloop()
