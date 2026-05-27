import os
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, askdirectory


class Window:
    def __init__(self, master):
        self.tree = None
        self.rootDir = None
        self.master = master
        self.ask_for_directory()

    def ask_for_directory(self):
        tk.Label(self.master, text="Welcome to MP3 Tagger!", font=("TkDefaultFont", 20)).grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self.master, text="Please select a root directory.", font=("TkDefaultFont", 15)).grid(row=1, column=0, padx=10, pady=5)
        self.rootDir = askdirectory()
        print(self.rootDir)
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

        tk.Button(self.master, text="Select", font=("TkDefaultFont", 15), command=self.treeview_select).grid(row=1, column=0, padx=10, pady=5)

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
            print("Item ID: ", current_item_id)

        filename_list.reverse()
        selected_filename = filename_list.pop(0)

        for i in filename_list:
            selected_filename = selected_filename + '\\' + i

        print("Filename: ", selected_filename)






def clear_window(master):
    for element in master.winfo_children():
        element.destroy()

def init():
    root = tk.Tk()
    window = Window(root)
    root.mainloop()