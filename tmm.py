'''
Trespasser Mod Manager (TMM) by MikeTheRaptor
The GUI-based mod manager for Trespasser CE
'''


VERSION_NUMBER = 'v0.3.8'


import logging
import os
from tkinter import (Tk, Label, Button, Listbox, Scrollbar, Menu, ttk,
    filedialog, messagebox, Checkbutton, IntVar, Toplevel, LabelFrame)
from configparser import ConfigParser
import shutil


logging.basicConfig(
    format='%(asctime)s - %(levelname)s:%(message)s',
    datefmt='%Y-%m-%d %I:%M',
    level=logging.INFO)


def backup_trespasser_ini():
    if os.path.exists('orig_trespasser.ini'):
        logging.info('orig_trespasser.ini already exists')
        pass
    else:
        orig = r'trespasser.ini'
        backup = r'orig_trespasser.ini'
        shutil.copy(orig, backup)
        logging.info('trespasser.ini backup created')

def create_tmm_ini():
    '''
    Create the file tmm_config.ini with blank values.
    '''
    parser = ConfigParser()
    parser.add_section('Paths')
    with open(r"tmm_config.ini", 'w') as configfile:
        parser.write(configfile)

def dependency_validation():
    '''
    Checks for files which the app is dependent on and displays appropriate error messages based on results.
    '''
    if os.path.exists('tp_mod.ini'):
        logging.info('dependency_validation says found tp_mod.ini')
    else:
        messagebox.showerror(
            'Trespasser Mod Manager - ERROR',
            'tp_mod.ini not found. Make sure that you are using Trespasser CE and that TMM.exe has been placed in the same directory as your Trespasser CE exe.')
        logging.critical('tp_mod.ini not found')
        raise SystemExit
    if os.path.exists('trespasser.ini'):
        logging.info('trespasser.ini found')
    else:
        messagebox.showerror('Trespasser Mod Manager - ERROR', 'trespasser.ini not found.')
        logging.critical('trespasser.ini not found')
        raise SystemExit

def launch_game():
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
        tmm_app.ce_exe_settings_prompt()

def get_active_mod():
    parser = ConfigParser()
    parser.read('tp_mod.ini')
    active_mod = parser['FM']['ActiveFM']
    logging.info('get_active_mod says the active mod is: ' + active_mod)
    return active_mod

def set_active_mod(selected_mod, label):
    '''
    Edits the tp_mod.ini to reflect the user's new mod choice.
    '''
    parser = ConfigParser()
    parser.read('tp_mod.ini')
    parser['FM']['ActiveFM'] = selected_mod
    with open('tp_mod.ini', 'w') as new_config_file:
        parser.write(new_config_file)
    label.config(text='Active Mod: '+ selected_mod)
    logging.info('set_active_mod says that the active mod has been changed to: ' + selected_mod)

def get_installed_mods():
    '''
    Return a list of all installed mods in fmpath directory
    '''
    parser = ConfigParser()
    parser.read('tp_mod.ini')
    mod_directory = parser['Paths']['fmpath']
    installed_mods = next(os.walk(mod_directory))[1]
    logging.info(next(os.walk(mod_directory))[1])
    return installed_mods

def get_mod_quality_setting():
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

def set_mod_quality_setting():
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

def get_ceoptions_setting(key, value):
    '''
    Gets value from key in trespasser.ini.
    '''
    parser = ConfigParser()
    parser.read('trespasser.ini')
    if parser.has_option(key, value) and (parser[key][value] == 'True' or parser[key][value] == 'true'):
        logging.info(f'{value} in {key} detected as True')
        return True
    elif parser.has_option(key, value) and (parser[key][value] == 'False' or parser[key][value] == 'false'):
        logging.info(f'{value} in {key} detected as False')
        return False
    else:
        logging.info(f'{value} in {key} NOT detected. Added {value} to {key}')
        parser[key][value] = 'False'
        with open(r"trespasser.ini", 'w') as configfile:
            parser.write(configfile)

def set_ceoptions_setting(key, value):
    parser = ConfigParser()
    parser.read('trespasser.ini')
    if parser.has_option(key, value) and (parser[key][value] == 'True' or parser[key][value] == 'true'):
        parser[key][value] = 'False'
        logging.info(f'{value} in {key} set to False')
    else:
        parser[key][value] = 'True'
        logging.info(f'{value} in {key} set to True')
    with open('trespasser.ini', 'w') as new_config_file:
        parser.write(new_config_file)


class MainApplication:
    def __init__(self, master):
        self.master = master
        dependency_validation()
        self.active_mod = get_active_mod()
        self.selected_mod = get_active_mod()
        self.configure_gui()
        backup_trespasser_ini()

        # ====== Create top menu ======

        # menubar = Menu(self.master)
        # file_menu = Menu(menubar, tearoff=0)
        # file_menu.add_command(label='Exit', command=self.master.destroy)
        # menubar.add_cascade(label='File', menu=file_menu)
        # self.master.config(menu=menubar)

        # ====== Create game launch button ======

        launch_button = Button(
            self.master,
            text='Launch Trespasser CE',
            command=lambda: launch_game())
        launch_button.pack(side='top', padx=5, pady=5)

        # ====== Create notebook tabs ======

        tabs_bar = ttk.Notebook(self.master)
        mods_frame = ttk.Frame(tabs_bar)
        ce_options_frame = ttk.Frame(tabs_bar)
        tabs_bar.add(mods_frame, text='Mods')
        tabs_bar.add(ce_options_frame, text='CE Options')
        tabs_bar.pack(expand=1, fill='both')

        # ====== Create mods_frame content ======

        active_mod_text = Label(
            mods_frame,
            text=f'Active Mod: {self.active_mod}')
        active_mod_text.pack(side='top')

        installed_mods_listbox = Listbox(mods_frame, height=10)
        for mod in get_installed_mods():
            installed_mods_listbox.insert('end', mod)
        installed_mods_listbox.pack(expand='true', side='top', fill='both', padx=10, pady=5)
        installed_mods_listbox_scrollbar = Scrollbar(installed_mods_listbox)
        installed_mods_listbox_scrollbar.pack(side='right', fill='y', expand='false')
        installed_mods_listbox.config(yscrollcommand=installed_mods_listbox_scrollbar.set)
        installed_mods_listbox_scrollbar.config(command=installed_mods_listbox.yview)
        installed_mods_listbox.bind('<<ListboxSelect>>', self.set_selected_mod)

        active_mod_changer_button = Button(
            mods_frame,
            text='Set Selected as Active Mod',
            command=lambda: set_active_mod(self.selected_mod, active_mod_text))
        active_mod_changer_button.pack(side='top')

        self.quality_var = IntVar()
        self.quality_var.set(get_mod_quality_setting())
        mod_quality_setting_toggle = Checkbutton(
            mods_frame,
            text='Use Recommended Quality Settings from Active Mod',
            variable=self.quality_var,
            onvalue=1,
            offvalue=0,
            command=set_mod_quality_setting)
        mod_quality_setting_toggle.pack(side='bottom')

        # ====== Create ce_options_frame content ======

        ce_options_label = Label(ce_options_frame, text='Basic CE Options')
        ce_options_label.grid(row=0, column=0, columnspan=2)

        # General Options Checkboxes

        general_label_frame = LabelFrame(ce_options_frame, text='General')
        general_label_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=10)
        ce_options_frame.columnconfigure(1, weight=1) # Makes LabelFrame fill app from left to right

        self.options_var_quicksave = IntVar()
        self.options_var_quicksave.set(get_ceoptions_setting('General', 'EnableQuickSaveKey'))
        options_ckbtn_quicksave = Checkbutton(
            general_label_frame,
            text='Set F9 as quicksave key',
            variable=self.options_var_quicksave,
            command=lambda: set_ceoptions_setting('General', 'EnableQuickSaveKey'))
        options_ckbtn_quicksave.grid(row=0, column=0, stick='w')

        self.options_var_dualstow = IntVar()
        self.options_var_dualstow.set(get_ceoptions_setting('General', 'EnableDualStow'))
        options_ckbtn_dualstow = Checkbutton(
            general_label_frame,
            text='Enable stowing two items at a time',
            variable=self.options_var_dualstow,
            command=lambda: set_ceoptions_setting('General', 'EnableDualStow'))
        options_ckbtn_dualstow.grid(row=1, column=0, sticky='w')

        # Display Options Checkboxes

        display_label_frame = LabelFrame(ce_options_frame, text='Display')
        display_label_frame.grid(row=2, column=0, columnspan=2, sticky='nsew', padx=10)
        ce_options_frame.columnconfigure(1, weight=1) # Makes LabelFrame fill app from left to right

        self.options_var_water = IntVar()
        self.options_var_water.set(get_ceoptions_setting('DisplayDX9', 'WaterRefraction'))
        options_ckbtn_water = Checkbutton(
            display_label_frame,
            text='Enable refractive water effect',
            variable=self.options_var_water,
            command=lambda: set_ceoptions_setting('DisplayDX9', 'WaterRefraction'))
        options_ckbtn_water.grid(row=0, column=0, stick='w')

        self.options_var_sky = IntVar()
        self.options_var_sky.set(get_ceoptions_setting('DisplayDX9', 'EnhancedSky'))
        options_ckbtn_sky = Checkbutton(
            display_label_frame,
            text='Enable new sky rendering method',
            variable=self.options_var_sky,
            command=lambda: set_ceoptions_setting('DisplayDX9', 'EnhancedSky'))
        options_ckbtn_sky.grid(row=1, column=0, sticky='w')

        # Render Options Checkboxes

        render_label_frame = LabelFrame(ce_options_frame, text='Render')
        render_label_frame.grid(row=3, column=0, columnspan=2, sticky='nsew', padx=10)
        ce_options_frame.columnconfigure(1, weight=1) # Makes LabelFrame fill app from left to right

        self.options_var_maxlod = IntVar()
        self.options_var_maxlod.set(get_ceoptions_setting('Render', 'ForceMaxObjectDetail'))
        options_ckbtn_maxlod = Checkbutton(
            render_label_frame,
            text='Force maximum level of detail',
            variable=self.options_var_maxlod,
            command=lambda: set_ceoptions_setting('Render', 'ForceMaxObjectDetail'))
        options_ckbtn_maxlod.grid(row=0, column=0, stick='w')

    def configure_gui(self):
        '''
        UI configuation settings.
        '''
        self.master.title(f'Trespasser Mod Manager {VERSION_NUMBER}')
#        self.master.iconbitmap(r'tmm_icon.ico') # Sets the icon inside the title bar
        self.master.geometry('400x300')
        self.master.resizable(False, False)
        self.master.eval('tk::PlaceWindow . center') # Centers the window

    def set_selected_mod(self, event):
        for i in event.widget.curselection():
            selected_mod = event.widget.get(i)
        logging.info(f'check_selected_mod says the selected mod is: {selected_mod}')
        self.selected_mod = selected_mod

    def ce_exe_settings_prompt(self):
        '''
        Generates a Toplevel window prompting the user to set EXE and FM paths.
        '''
        create_tmm_ini()
        settings_window = Toplevel()
        settings_window.title("Trespasser Mod Manager - Configuration")
        settings_window.resizable('False','False')
        self.master.eval(f'tk::PlaceWindow {str(settings_window)} center')
        settings_window.grab_set()
        settings_label = Label(
            master=settings_window,
            justify='left',
            wraplength=400,
            text="Your Trespasser CE exe hasn't been configured yet.\nFind your Trespasser CE exe file, press save, and try again.")
        settings_label.grid(column=0, row=0, columnspan=1, sticky='w', padx=10, pady=(10,0))
        exe_path_label = Label(master=settings_window, text="Trespasser CE exe path:")
        exe_path_label.grid(column=0, row=1, sticky='w', padx=10, pady=(10,0))
        exe_path_label2 = Label(master=settings_window, width=60, relief='sunken')
        exe_path_label2.grid(column=0, row=2, sticky='w', padx=(10,0), pady=(0,10))
        exe_path_button = Button(
            master=settings_window,
            text='...',
            command=lambda: self.get_exe_path(exe_path_label2))
        exe_path_button.grid(column=1, row=2, sticky='w', padx=(0, 10))
        settings_save_button = Button(
            master=settings_window,
            text="Save",
            command=lambda: self.set_exe_path(settings_window))
        settings_save_button.grid(column=3, row=3, sticky='se', padx=10, pady=10)

    def get_exe_path(self, label):
        '''
        Opens file browser window for user selection of Tres CE exe path and updates label with path.
        '''
        self.exe_path = filedialog.askopenfilename(
            initialdir='./',
            title='Select Trespasser CE EXE',
            filetypes=[('Trespasser CE','*.exe')])
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
        logging.info('Exe path has been set')
        window.destroy()


if __name__ == '__main__':
    root = Tk()
    tmm_app = MainApplication(root)
    root.mainloop()
    