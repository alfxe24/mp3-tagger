import os
import tkinter as tk
from pathlib import Path
from tkinter import ttk
from tkinter.filedialog import askopenfilename, askdirectory
import glob
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
import mutagen.id3
from mutagen.id3 import ID3, TIT2, TIT3, TALB, TPE1, TRCK, TYER

def clear_window(master):
    for element in master.winfo_children():
        element.destroy()

def glob_to_array(files):
    files_list = []
    for i in range(0, len(files)):
        files_list.append(MP3(files[i], ID3=EasyID3))
    return files_list

def stringify_filenames(string):
    '''
    Ref for Fix:
    https://github.com/nushell/nushell/issues/10244
    '''
    string = string.replace("[", "[[]")
    string = string.replace("]", "[]]")
    string = string.replace("[[[]]", "[[]")

    return string


class Window:
    def __init__(self, master):
        self.tree = None
        self.rootDir = None
        self.master = master
        self.ask_for_directory()
        self.current_settings = None

    def ask_for_directory(self):
        tk.Label(self.master, text="Welcome to MP3 Tagger!", font=("TkDefaultFont", 20)).grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self.master, text="Please select a root directory.", font=("TkDefaultFont", 15)).grid(row=1, column=0, padx=10, pady=5)
        self.rootDir = askdirectory()
        self.show_treeview()

    def show_treeview(self):
        """
        Ref:
        https://stackoverflow.com/questions/16746387/display-directory-content-with-tkinter-treeview-widget
        """
        clear_window(self.master)
        self.tree = ttk.Treeview()
        ysb = ttk.Scrollbar(self.master, orient='vertical', command=self.tree.yview)
        xsb = ttk.Scrollbar(self.master, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)
        self.tree.heading('#0', text=self.rootDir, anchor='w')

        abspath = os.path.abspath(self.rootDir)
        root_node = self.tree.insert('', 'end', text=abspath, open=True)
        self.process_directory(root_node, abspath)

        self.tree.grid(row=0, column=0)
        ysb.grid(row=0, column=1, sticky='ns')
        xsb.grid(row=1, column=0, sticky='ew')

        tk.Button(self.master, text="Select", font=("TkDefaultFont", 15), command=self.treeview_select).grid(row=2, column=0, padx=10, pady=5)

    def process_directory(self, parent, path):
        for p in os.listdir(path):
            abspath = os.path.join(path, p)
            isdir = os.path.isdir(abspath)
            oid = self.tree.insert(parent, 'end', text=p, open=False)
            if isdir:
                self.process_directory(oid, abspath)

    def treeview_select(self):
        item_id = self.tree.selection()

        filename_list = []
        current_item_id = item_id

        while current_item_id is not '':
            filename_list.append(self.tree.item(current_item_id, 'text'))
            current_item_id = self.tree.parent(current_item_id)

        filename_list.reverse()
        selected_filename = filename_list.pop(0)

        for i in filename_list:
            selected_filename = selected_filename + '\\' + i

        selected_filename = stringify_filenames(selected_filename)

        self.change_settings(selected_filename)

    def change_settings(self, filename):
        clear_window(self.master)

        try:
            files = glob.glob(filename + "/*.mp3")
            print("Files D: ", files)
        except:
            files = glob.glob(filename)
            print("Files F: ", files)

        file_elements = glob_to_array(files)

        self.display_settings_page(files)

    def display_settings_page(self, files):
        # tk.Label(self.master,)
        self.current_settings = Settings(len(files))

        tk.Label(self.master, text="Filename").grid(row=0, column=0, padx=3, pady=3)
        tk.Label(self.master, text="Album Artist").grid(row=0, column=1, padx=3, pady=3)
        tk.Label(self.master, text="Title").grid(row=0, column=2, padx=3, pady=3)
        tk.Label(self.master, text="Track Number (x/y)").grid(row=0, column=3, padx=3, pady=3)
        tk.Label(self.master, text="Genre").grid(row=0, column=4, padx=3, pady=3)
        tk.Label(self.master, text="Album").grid(row=0, column=5, padx=3, pady=3)
        tk.Label(self.master, text="Artist").grid(row=0, column=6, padx=3, pady=3)
        tk.Label(self.master, text="Year").grid(row=0, column=7, padx=3, pady=3)

        for row in range(len(files)):
            tk.Label(self.master, text=files[row]).grid(row=row+1, column=0, padx=3, pady=3)
            tk.Entry(self.master, textvariable=self.current_settings.album_artist_list[row]).grid(row=row+1, column=1, padx=3, pady=3)
            tk.Entry(self.master, textvariable=self.current_settings.title_list[row]).grid(row=row+1, column=2, padx=3, pady=3)
            tk.Entry(self.master, textvariable=self.current_settings.track_number_list[row]).grid(row=row+1, column=3, padx=3, pady=3)
            tk.Entry(self.master, textvariable=self.current_settings.genre_list[row]).grid(row=row+1, column=4, padx=3, pady=3)
            tk.Entry(self.master, textvariable=self.current_settings.album_list[row]).grid(row=row+1, column=5, padx=3, pady=3)
            tk.Entry(self.master, textvariable=self.current_settings.artist_list[row]).grid(row=row+1, column=6, padx=3, pady=3)
            tk.Entry(self.master, textvariable=self.current_settings.date_list[row]).grid(row=row+1, column=7, padx=3, pady=3)

        tk.Button(self.master, command=self.submit_settings, text="Submit").grid(row=len(files)+1, column=0, columnspan=8, pady=5)

    def submit_settings(self):
        return

class Settings:
    def __init__(self, length):
        self.album_artist_list = []
        self.title_list = []
        self.track_number_list = []
        self.genre_list = []
        self.album_list = []
        self.artist_list = []
        self.date_list = []

        for i in range(length):
            self.album_artist_list.append(tk.StringVar())
            self.title_list.append(tk.StringVar())
            self.track_number_list.append(tk.StringVar())
            self.genre_list.append(tk.StringVar())
            self.album_list.append(tk.StringVar())
            self.artist_list.append(tk.StringVar())
            self.date_list.append(tk.StringVar())

def init():
    root = tk.Tk()
    window = Window(root)
    root.mainloop()