
#Trespasser Mod Manager (TMM)
version_number = 'v0.3.6'

import logging
import os
from tkinter import Tk, Label, Button, Listbox, Scrollbar, Menu, ttk, filedialog, messagebox, Checkbutton, IntVar, Toplevel, Entry
from configparser import ConfigParser

logging.basicConfig(format='%(asctime)s - %(levelname)s:%(message)s', datefmt='%Y-%m-%d %I:%M', level=logging.INFO)

class MainApplication:
    def __init__(self, master):
        self.master = master
        self.active_mod = 'not set'
        self.selected_mod = 'not set'
        self.dependency_validation()
        self.get_active_mod()
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
        for mod in self.get_installed_mods():
            installed_mods_listbox.insert('end', mod)
        installed_mods_listbox.pack(expand='true', side='top', fill='both')
        installed_mods_listbox_scrollbar = Scrollbar(installed_mods_listbox)
        installed_mods_listbox_scrollbar.pack(side='right', fill='y', expand='false')
        installed_mods_listbox.bind('<<ListboxSelect>>', self.set_selected_mod)

        active_mod_changer_button = Button(self.master, text='Set as Active Mod', command=lambda: self.set_active_mod(self.selected_mod, active_mod_text))
        active_mod_changer_button.pack(side='bottom')

        self.quality_var = IntVar()
        self.quality_var.set(self.get_mod_quality_setting())
        mod_quality_setting_toggle = Checkbutton(self.master, text='Use Recommended Quality Settings from Active Mod', variable=self.quality_var, onvalue=1, offvalue=0, command=self.set_mod_quality_setting)
        mod_quality_setting_toggle.pack(side='bottom')

    def configure_gui(self):
        '''
        UI configuation settings.
        '''
        self.master.title('Trespasser Mod Manager ' + version_number)
#        self.master.iconbitmap(r'tmm_icon.ico')
        self.master.geometry('400x300')
        self.master.resizable(False, False)
        self.master.eval('tk::PlaceWindow . center')        # centers the window

    def launch_game(self):
        '''
        Opens a dialogue window with a file browser allowing the user to select their Trespasser CE EXE file and then launches the file.
        '''
        parser = ConfigParser()
        parser.read('tmm_config.ini')
        if os.path.exists('tmm_config.ini') and parser.has_option('Paths', 'exepath') and (os.path.exists(parser['Paths']['exepath'])):
            logging.info("launch_game says: Launching game")
            os.startfile(parser['Paths']['exepath'])
        else:
            logging.info("launch_game says: Trespasser CE exe not configured.")
            self.ce_exe_settings_prompt()

#    def create_tabs(self):
#        '''
#        Creates a tab for containing settings toggles for the trespasser.ini.
#        '''
#        tabs_bar = ttk.Notebook(self.master)
#        mods_tab = ttk.Frame(tabs_bar)
#        ce_settings_tab = ttk.Frame(tabs_bar)
#        tabs_bar.add(mods_tab, text='Mods')
#        tabs_bar.add(ce_settings_tab, text='CE Settings')
#        tabs_bar.pack(expand=1, fill='both')

    def set_active_mod(self, selected_mod, label):
        '''
        Edits the tp_mod.ini to reflect the user's new mod choice.
        '''
        parser = ConfigParser()
        parser.read('tp_mod.ini')
        parser['FM']['ActiveFM'] = selected_mod
        if parser.has_option('FM', 'UseRecommendedQuality'):
            parser['FM']['UseRecommendedQuality'] = parser['FM']['UseRecommendedQuality']   #preserves the user's original UseRecommendedQuality setting
        with open('tp_mod.ini', 'w') as new_config_file:
            parser.write(new_config_file)
        label.config(text='Active Mod: '+ selected_mod)
        logging.info('set_active_mod says that the active mod has been changed to: ' + selected_mod)

    def get_active_mod(self):
        parser = ConfigParser()
        parser.read('tp_mod.ini')
        active_mod = parser['FM']['ActiveFM']
        logging.info('get_active_mod says the active mod is: ' + active_mod)
        self.active_mod = active_mod

    def get_installed_mods(self):
        '''
        Checks the user's tp_mod.ini to determine the fmpath folder, then checks all directories in the fmpath folder to generate a list of which mods are installed.
        '''
        parser = ConfigParser()
        parser.read('tp_mod.ini')
        mod_directory = parser['Paths']['fmpath']
        installed_mods = next(os.walk(mod_directory))[1]
        logging.info(next(os.walk(mod_directory))[1])
        return installed_mods

    def set_selected_mod(self, event):
        for i in event.widget.curselection():
            selected_mod = event.widget.get(i)
        logging.info('check_selected_mod says the selected mod is: ' + selected_mod)
        self.selected_mod = selected_mod

    def get_mod_quality_setting(self):
        '''
        Gets the user's tp_mod.ini UseRecommendedQuality setting.
        '''
        parser = ConfigParser()
        parser.read('tp_mod.ini')
        if parser.has_option('FM','UseRecommendedQuality') and (parser['FM']['UseRecommendedQuality'] == 'true'):
            mod_quality_setting = parser['FM']['UseRecommendedQuality']
            logging.info('get_mod_quality_setting says the quality setting is: ' + mod_quality_setting)
            return True
        else:
            return False

    def set_mod_quality_setting(self):
        '''
        Sets the user's tp_mod.ini UseRecommendedQuality setting to true or false.
        '''
        logging.info('UseRecommendedQuality checkbox clicked')
        parser = ConfigParser()
        parser.read('tp_mod.ini')
        if parser.has_option('FM','UseRecommendedQuality') and (parser['FM']['UseRecommendedQuality'] == 'true'):
            parser['FM']['UseRecommendedQuality'] = 'false'
            logging.info('UseRecommendedQuality set to FALSE')
        else:
            parser['FM']['UseRecommendedQuality'] = 'true'
            logging.info('UseRecommendedQuality set to TRUE')
        with open('tp_mod.ini', 'w') as new_config_file:
            parser.write(new_config_file)

    def ce_exe_settings_prompt(self):
        '''
        Generates a Toplevel window prompting the user to set EXE and FM paths.
        '''
        self.create_ini()
        settings_window = Toplevel()
        settings_window.title("Trespasser Mod Manager - Configuration")
        settings_window.resizable('False','False')
        self.master.eval(f'tk::PlaceWindow {str(settings_window)} center')
        settings_window.grab_set()
        settings_label = Label(master=settings_window, justify='left', wraplength=400, text="Your Trespasser CE exe hasn't been configured yet.\nFind your Trespasser CE exe file, press save, and try again.")
        settings_label.grid(column=0, row=0, columnspan=1, sticky='w', padx=10, pady=(10,0))
        exe_path_label = Label(master=settings_window, text="Trespasser CE Exe Path:")
        exe_path_label.grid(column=0, row=1, sticky='w', padx=10, pady=(10,0))
        exe_path_label2 = Label(master=settings_window, width=60, relief='sunken')
        exe_path_label2.grid(column=0, row=2, sticky='w', padx=(10,0), pady=(0,10))
        exe_path_button = Button(master=settings_window, text='...', command=lambda: self.get_exe_path(exe_path_label2))
        exe_path_button.grid(column=1, row=2, sticky='w', padx=(0, 10))
        settings_save_button = Button(master=settings_window, text="Save", command=lambda: self.set_exe_path(settings_window))
        settings_save_button.grid(column=3, row=3, sticky='se', padx=10, pady=10)
    
    def create_ini(self):
        '''
        Create the file tmm_config.ini with blank values.
        '''
        parser = ConfigParser()
        parser.add_section('Paths')
        with open(r"tmm_config.ini", 'w') as configfile:
            parser.write(configfile)

    def get_exe_path(self, label):
        '''
        Opens file browser window for user selection of Tres CE exe path and updates label with path.
        '''
        self.exe_path = filedialog.askopenfilename(initialdir='./', title='Select Trespasser CE EXE', filetypes=[('Trespasser CE','*.exe')])
        label.config(text=self.exe_path)

    def set_exe_path(self, window):
        '''
        Saves user selected Tres CE exe path to tmm_config.ini and closes window.
        '''
        parser = ConfigParser()
        parser.read('tmm_config.ini')
        parser['Paths']['exepath'] = self.exe_path
        with open(r"tmm_config.ini", 'w') as configfile:
            parser.write(configfile)
        window.destroy()

    def dependency_validation(self):
        '''
        Checks for files which the app is dependent on and displays appropriate error messages based on results.
        '''
        if os.path.exists('tp_mod.ini'):
            logging.info('dependency_validation says found tp_mod.ini')
        else:
            messagebox.showerror('Trespasser Mod Manager - ERROR', 'tp_mod.ini not found. Make sure that you are using Trespasser CE and that TMM.exe has been placed in the same directory as your Trespasser CE exe.')
            logging.critical('tp_mod.ini not found')
            raise SystemExit

if __name__ == '__main__':
    root = Tk()
    tmm_app = MainApplication(root)
    root.mainloop()
    