'''
Trespasser Mod Manager (TMM) by MikeTheRaptor
The GUI-based mod manager for Trespasser CE
'''

VERSION_NUMBER = 'v0.5.0'

from configparser import ConfigParser
import logging
from tkinter import Tk, ttk, Listbox
import os


logging.basicConfig(
    format='%(asctime)s - %(levelname)s:%(message)s',
    datefmt='%Y-%m-%d %I:%M',
    level=logging.INFO)


def get_mods():
    parser = ConfigParser()
    parser.read('tp_mod.ini')
    mod_path = parser['Paths']['fmpath']
    dir_names = next(os.walk(mod_path))[1]
    installed_mods = []
    for dir in dir_names:
        installed_mods.append(Mod(dir))
    return installed_mods


class Mod:
    def __init__(self, name):
        self.name = name

class TMMListbox():
    '''
    Generates a Listbox widget containing mod names.
    '''
    def __init__(self, master, list, row, col):
        lb = Listbox(master, height=10)
        for obj in list:
            lb.insert('end', obj.name)
        lb.grid(row=row, column=col)

class TMMNotebook():
    def __init__(self, master, row, col):
        tabs = ttk.Notebook(master)
        self.mods_frm = ttk.Frame(tabs)
        self.options_frm = ttk.Frame(tabs)
        tabs.add(self.mods_frm, text='Mods')
        tabs.add(self.options_frm, text='CE Options')
        tabs.grid(row=row, column=col)

    def get_frm(self, frame):
        if frame == 'mods':
            return self.mods_frm
        elif frame == 'options':
            return self.options_frm



class MainApplication:
    def __init__(self, master):
        self.master = master

        # ====== Configure GUI ======

        # ====== Create notebook tabs ======

        tabs = TMMNotebook(master, 0, 0)

        # ====== Create mods tab content ======

        #  Create List of Installed Mod Objects

        installed_mods = get_mods()

        # Create Listbox showing Installed Mod Object Names

        mods_lb = TMMListbox(tabs.get_frm('mods'), installed_mods, 0, 0)







if __name__ == '__main__':
    root = Tk()
    tmm_app = MainApplication(root)
    root.mainloop()