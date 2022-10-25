
#Trespasser Mod Manager (TMM)
version_number = 'v0.3.2'

import os
from tkinter import Tk, Label, Button, Listbox, Scrollbar, Menu, ttk
from configparser import ConfigParser

class MainApplication:
    def __init__(self, master):
        self.master = master
        self.active_mod = 'not set'
        self.selected_mod = 'not set'
        self.set_active_mod()
        self.configure_gui()

        menubar = Menu(self.master)
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label='Exit', command=self.master.destroy)
        menubar.add_cascade(label='File', menu=file_menu)
        self.master.config(menu=menubar)

        launch_button = Button(self.master, text='Launch Trespasser CE', command=lambda: self.launch_game())
        launch_button.pack(side='top')

        active_mod_text = Label(self.master, text='Active Mod: ' + self.active_mod)
        active_mod_text.pack(side='top')

        installed_mods_listbox = Listbox(self.master, height=10)
        for mod in self.check_installed_mods():
            installed_mods_listbox.insert('end', mod)
        installed_mods_listbox.pack(expand='true', side='top', fill='both')
        installed_mods_listbox_scrollbar = Scrollbar(installed_mods_listbox)
        installed_mods_listbox_scrollbar.pack(side='right', fill='y', expand='false')
        installed_mods_listbox.bind('<<ListboxSelect>>', self.set_selected_mod)

        active_mod_changer_button = Button(self.master, text='Set as Active Mod', command=lambda: self.change_active_mod(self.selected_mod, active_mod_text))
        active_mod_changer_button.pack(side='bottom')

    def configure_gui(self):
        self.master.title('Trespasser Mod Manager ' + version_number)
#        self.master.iconbitmap(r'tmm_icon.ico')
        self.master.geometry('400x300')
        self.master.resizable(False, False)

    def launch_game(self):
        print('launch_game says: Launching game')
        os.startfile('TresCE.exe')

# The following creates a tab for containing settings toggles for the trespasser.ini.
#    def create_tabs(self):
#        tabs_bar = ttk.Notebook(self.master)
#        mods_tab = ttk.Frame(tabs_bar)
#        ce_settings_tab = ttk.Frame(tabs_bar)
#        tabs_bar.add(mods_tab, text='Mods')
#        tabs_bar.add(ce_settings_tab, text='CE Settings')
#        tabs_bar.pack(expand=1, fill='both')

    def change_active_mod(self, selected_mod, label):
        parser = ConfigParser()
        parser.read('tp_mod.ini')
        parser['FM']['ActiveFM'] = selected_mod
        with open('tp_mod.ini', 'w') as new_config_file:
            parser.write(new_config_file)
        label.config(text='Active Mod: '+ selected_mod)
        print('change_active_mod says that the active mod has been changed to: ' + selected_mod)

    def set_active_mod(self):
        parser = ConfigParser()
        parser.read('tp_mod.ini')
        active_mod = parser['FM']['ActiveFM']
        print('set_active_mod says the active mod is: ' + active_mod)
        self.active_mod = active_mod

    def check_installed_mods(self):
        parser = ConfigParser()
        parser.read('tp_mod.ini')
        mod_directory = parser['Paths']['fmpath']
        print('check_installed_mods says that the mod directory is: ' + mod_directory)
        installed_mods = os.listdir(mod_directory)
        print('check_installed_mods says the installed mods are:', end=' ')
        print(os.listdir(mod_directory))
        return installed_mods

    def set_selected_mod(self, event):
        for i in event.widget.curselection():
            selected_mod = event.widget.get(i)
        print('check_selected_mod says the selected mod is: ' + selected_mod)
        self.selected_mod = selected_mod


if __name__ == '__main__':
    root = Tk()
    tmm_app = MainApplication(root)
    root.mainloop()
    