'''
Trespasser Mod Manager (TMM) by MikeTheRaptor
The GUI-based mod manager for Trespasser CE
'''

VERSION_NUMBER = 'v1.0.0'

from configparser import ConfigParser
import logging
import os
import shutil
from tkinter import (
    Button,
    Canvas,
    constants,
    Checkbutton,
    filedialog,
    Frame,
    IntVar,
    Label,
    LabelFrame,
    Listbox,
    Menu,
    messagebox,
    Text,
    Tk,
    Toplevel,
    ttk,
    Scrollbar
    )
import zipfile


def validation():
    '''
    Checks for dependencies and throws exceptions or launches app
    '''
    if not os.path.exists('tp_mod.ini'):
        messagebox.showerror(
            'Trespasser Mod Manager - ERROR',
            'tp_mod.ini not found.\nMake sure that you are using Trespasser CE and that TMM.exe has been placed in the same directory as your Trespasser CE exe.')
        logging.critical('tp_mod.ini not found')
        raise SystemExit
    elif not os.path.exists('trespasser.ini'):
        messagebox.showerror('Trespasser Mod Manager - ERROR', 'trespasser.ini not found.\nMake sure that you are using Trespasser CE and that TMM.exe has been placed in the same directory as your Trespasser CE exe.')
        logging.critical('trespasser.ini not found')
        raise SystemExit
    else:
        logging.info('tp_mod.ini and trespasser.ini found')


# Initialize Logging Settings
logging.basicConfig(
    format='%(asctime)s - %(levelname)s:%(message)s',
    datefmt='%Y-%m-%d %I:%M',
    level=logging.INFO)

class FirstTimeSetup(Toplevel):
    def __init__(self):
        pass

class MainApplication:
    def __init__(self, parent, *args, **kwargs):

        # Initialization
        self.parent = parent
        self.selected_mod = self.get_active_mod()
        self.active_mod = self.get_active_mod()
        self.launch_on_save = False
        self.backup_trespasser_ini()


        # Configure Main Window
        self.parent.title(f'Trespasser Mod Manager {VERSION_NUMBER}')
        self.parent.resizable(False, False)

        # ====== Create top menu ======

        menubar = Menu(self.parent)
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label='Settings', command=self.open_settings)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.parent.destroy)
        menubar.add_cascade(label='File', menu=file_menu)

        install_menu = Menu(menubar, tearoff=0)
        install_menu.add_command(label='Trespasser Retail from Disc', command=self.install_retail)
        install_menu.add_command(label='Mod from Zip file', command=self.install_mfz)
        menubar.add_cascade(label='Install...', menu=install_menu)

        self.parent.config(menu=menubar)

        # ====== Create header ====== #

        separator = ttk.Separator(parent, orient='horizontal')
        separator.grid(row=0, column=0, sticky='we')

        launch_btn = Button(parent, command=self.launch_game, text='Launch Trespasser CE')
        launch_btn.grid(row=1, column=0, padx=10, pady=(10,5))

        amod_lbl = Label(text=f'Active: {self.active_mod}')
        amod_lbl.grid(row=2, column=0)

        separator = ttk.Separator(parent, orient='horizontal')
        separator.grid(row=3, column=0, sticky='we', pady=5)

        # ====== Create notebook tabs ======

        tabs_bar = ttk.Notebook(parent, padding=5)
        mods_frm = ttk.Frame(tabs_bar, padding=10)
        options_frm = ttk.Frame(tabs_bar, padding=10)
        tabs_bar.add(mods_frm, text='Mods')
        tabs_bar.add(options_frm, text='CE Options')
        tabs_bar.grid(row=4, column=0)

        # ====== Create Mods tab content ======

        # === Installed Mods Frame ===

        imods_lfrm = LabelFrame(mods_frm, text='Installed Mods')
        imods_lfrm.grid(row=0, column=0, padx=(0, 2.5))

        # Listbox & Scrollbar

        mods_lb = Listbox(imods_lfrm, height=10)
        mods_sb = Scrollbar(imods_lfrm)
        mods_lb.config(yscrollcommand=mods_sb.set)
        mods_sb.config(command=mods_lb.yview)
        mods_lb.grid(row=0, column=0, padx=(5,0), pady=5)
        mods_sb.grid(row=0, column=1, padx=(0,5), pady=2.5, sticky='ns')
        mods_lb.bind('<<ListboxSelect>>', self.set_selected_mod)

        # Populate Listbox

        imods_lst = self.get_installed_mods()
        for mod in imods_lst:
            mods_lb.insert('end', mod)

        # Active Mod Button

        set_mod_btn = Button(imods_lfrm, text='Set Active Mod', command=lambda: self.set_active_mod(self.selected_mod, amod_lbl))
        set_mod_btn.grid(row=1, column=0, columnspan=2, padx=5, pady=(2.5,5))

        # === Selected Mod Frame ===

        smod_lfrm = LabelFrame(mods_frm, text='Selected Mod Info')
        smod_lfrm.grid(row=0, column=1, padx=(2.5, 0))

        # Mod Info Text

        global info_txt
        info_txt = Text(smod_lfrm, height=10, width=30, bg='#F3F3F3')
        info_txt.insert(constants.INSERT, "No Mod Selected")
        info_txt.config(state='disabled')
        info_txt.grid(row=0, column=0, padx=(5, 0), pady=5)
        info_sb = Scrollbar(smod_lfrm, command=info_txt.yview)
        info_sb.grid(row=0, column=2, padx=(0, 5), pady=2.5, sticky='ns')
        info_txt.configure(yscrollcommand=info_sb.set)

        # Mod Quality Checkbutton

        self.quality_var = IntVar()
        self.quality_var.set(self.get_quality())
        quality_cb = Checkbutton(
            smod_lfrm,
            variable=self.quality_var,
            onvalue=1,
            offvalue=0,
            text='Use Recommended Quality Settings',
            command=self.set_quality)
        quality_cb.grid(row=1, column=0, columnspan=2, padx=5, pady=(2.5,5.5))

        # ====== Create CE Options tab content ======

        # === Generate Scrollable Frame ===

        # CE Options Canvas (required for scrolling)

        options_cnvs = Canvas(options_frm, highlightthickness=0, height=225, width=420)
        options_cnvs.grid(row=0, column=0)
        options_cnvs.grid_columnconfigure(0)
        options_cnvs.grid_rowconfigure(0)
        options_cnvs.grid_propagate(False) # prevents the canvas from expanding or shrinking to fit contents

        # CE Options Scrollbar

        options_sb = Scrollbar(options_frm, command=options_cnvs.yview)
        options_sb.grid(row=0, column=1, sticky='ns')
        options_cnvs.configure(yscrollcommand=options_sb.set)
        options_cnvs.bind('<Configure>', lambda e: options_cnvs.configure(scrollregion=options_cnvs.bbox("all")))

        # CE Options Inner Library Frame (required for scrolling)

        options_ifrm = Frame(options_cnvs)
        options_cnvs.create_window((0, 0), window=options_ifrm, anchor='nw')

        # === Generate Options Widgets ===

        # = General Options =

        general_lfrm = LabelFrame(options_ifrm, text='General')
        general_lfrm.grid(row=0, column=0, sticky='we')

        # Quicksave Checkbutton

        self.ce_quicksave_var = IntVar()
        self.ce_quicksave_var.set(self.get_ceoption_bool('General', 'EnableQuickSaveKey'))
        ce_quicksave_cb = Checkbutton(
            general_lfrm,
            variable=self.ce_quicksave_var,
            command=lambda: self.set_ceoption_bool('General', 'EnableQuickSaveKey'),
            text='Set F9 as quicksave key'
        )
        ce_quicksave_cb.grid(row=0, column=0, sticky='w')

        # Dualstow Checkbutton

        self.ce_dualstow_var = IntVar()
        self.ce_dualstow_var.set(self.get_ceoption_bool('General', 'EnableDualStow'))
        ce_dualstow_cb = Checkbutton(
            general_lfrm,
            variable=self.ce_dualstow_var,
            command=lambda: self.set_ceoption_bool('General', 'EnableDualStow'),
            text='Enable stowing two items at a time'
        )
        ce_dualstow_cb.grid(row=1, column=0, sticky='w')

        # = Display Options =

        display_lfrm = LabelFrame(options_ifrm, text='Display')
        display_lfrm.grid(row=1, column=0, sticky='nsew')

        # Water Checkbutton

        self.ce_water_var = IntVar()
        self.ce_water_var.set(self.get_ceoption_bool('DisplayDX9', 'WaterRefraction'))
        ce_water_cb = Checkbutton(
            display_lfrm,
            variable=self.ce_water_var,
            command=lambda: self.set_ceoption_bool('DisplayDX9', 'WaterRefraction'),
            text='Enable refractive water effect'
        )
        ce_water_cb.grid(row=0, column=0, sticky='w')

        # Sky Checkbutton

        self.ce_sky_var = IntVar()
        self.ce_sky_var.set(self.get_ceoption_bool('DisplayDX9', 'EnhancedSky'))
        ce_sky_cb = Checkbutton(
            display_lfrm,
            variable=self.ce_sky_var,
            command=lambda: self.set_ceoption_bool('DisplayDX9', 'EnhancedSky'),
            text='Enable new sky rendering method'
        )
        ce_sky_cb.grid(row=1, column=0, sticky='w')

        # = Render Options =

        render_lfrm = LabelFrame(options_ifrm, text='Render')
        render_lfrm.grid(row=2, column=0, sticky='nsew')

        # ForceMaxObjectDetail Checkbutton

        self.ce_maxlod_var = IntVar()
        self.ce_maxlod_var.set(self.set_ceoption_bool('Render', 'ForceMaxObjectDetail'))
        ce_maxlod_cb = Checkbutton(
            render_lfrm,
            variable=self.ce_maxlod_var,
            command=lambda: self.set_ceoption_bool('Render', 'ForceMaxObjectDetail'),
            text='Force maximum level of detail'
        )
        ce_maxlod_cb.grid(row=0, column=0, sticky='w')     

    # ====== TMM Functions ======

    # === Selected Mod Functions ===

    def set_selected_mod(self, event):
        '''
        Sets the selected mod and populates the mod info textbox.
        '''
        for i in event.widget.curselection():
            selected_mod = event.widget.get(i)
        logging.info(f'{selected_mod} selected')
        self.selected_mod = selected_mod
        if os.path.exists(f'mods/{selected_mod}/info.txt'):
            logging.info(f'Info text found for {selected_mod}')
            info_txt.config(state='normal')
            with open(f'mods/{selected_mod}/info.txt') as file:
                contents = file.read()
                info_txt.delete('1.0', 'end')
                info_txt.insert('1.0', contents)
                info_txt.config(state='disabled')
        else:
            logging.info(f'Info text not found for {selected_mod}')
            info_txt.config(state='normal')
            info_txt.delete('1.0', 'end')
            info_txt.insert('1.0', 'No Mod Info')
            info_txt.config(state='disabled')

    # === trespasser.ini Functions ===

    def backup_trespasser_ini(self):
        '''
        Creates a one-time backup of the trespasser.ini
        '''
        if os.path.exists('orig_trespasser.ini'):
            logging.info('orig_trespasser.ini already exists')
            pass
        else:
            orig = r'trespasser.ini'
            backup = r'orig_trespasser.ini'
            shutil.copy(orig, backup)
            logging.info('trespasser.ini backup created')

    def get_ceoption_bool(self, key, value):
        '''
        Gets bool value from key in trespasser.ini.
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

    def set_ceoption_bool(self, key, value):
        '''
        Sets bool value for key in trespasser.ini.
        '''
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

    # === tp_mod.ini Functions ===

    def get_active_mod(self):
        parser = ConfigParser()
        parser.read('tp_mod.ini')
        active_mod = parser['FM']['ActiveFM']
        return active_mod

    def set_active_mod(self, selected_mod, label):
        parser = ConfigParser()
        parser.read('tp_mod.ini')
        parser['FM']['ActiveFM'] = selected_mod
        with open('tp_mod.ini', 'w') as new_config_file:
            parser.write(new_config_file)
        label.config(text='Active Mod: '+ selected_mod)
        logging.info(f'{selected_mod} set to active')

    def get_fmpath(self):
        parser = ConfigParser()
        parser.read('tp_mod.ini')
        fmpath = parser['Paths']['fmpath']
        return fmpath

    def get_installed_mods(self):
        parser = ConfigParser()
        parser.read('tp_mod.ini')
        installed_mods = next(os.walk(self.get_fmpath()))[1]
        return installed_mods

    def get_quality(self):
        '''
        Gets UseRecommendedQuality from tp_mod.ini
        '''
        parser = ConfigParser()
        parser.read('tp_mod.ini')
        if parser.has_option('FM','UseRecommendedQuality') and (parser['FM']['UseRecommendedQuality'] == 'true'):
            mod_quality_setting = parser['FM']['UseRecommendedQuality']
            logging.info(f'UseRecommendedQuality in tp_mod.ini is {mod_quality_setting}')
            return True
        else:
            return False

    def set_quality(self):
        '''
        Sets UseRecommendedQuality in tp_mod.ini
        '''
        logging.info('UseRecommendedQuality checkbox clicked')
        parser = ConfigParser()
        parser.read('tp_mod.ini')
        if parser.has_option('FM','UseRecommendedQuality') and (parser['FM']['UseRecommendedQuality'] == 'true'):
            parser['FM']['UseRecommendedQuality'] = 'false'
            logging.info('UseRecommendedQuality in tp_mod.ini set to False')
        else:
            parser['FM']['UseRecommendedQuality'] = 'true'
            logging.info('UseRecommendedQuality in tp_mod.ini set to True')
        with open('tp_mod.ini', 'w') as new_config_file:
            parser.write(new_config_file)

    # === tmm.ini Functions ===

    def launch_game(self):
        parser = ConfigParser()
        parser.read('tmm.ini')
        if os.path.exists('tmm.ini') and parser.has_option('Paths', 'exepath'):
            logging.info('Launching game')
            os.startfile(parser['Paths']['exepath'])
        else:
            logging.info('tmm.ini and/or exe path not detected.')
            self.launch_on_save = True # Track if settings was opened via Launch button
            self.open_settings()

    def get_exepath(self, label):
        '''
        Open file browser window for user selection of Tres CE exe path.
        '''
        self.exe_path = filedialog.askopenfilename(
            initialdir='./',
            title='Select Trespasser CE EXE',
            filetypes=[('Trespasser CE','*.exe')]
        )
        label.config(text=self.exe_path)

    def save_settings(self, window):
        '''
        Saves Tres CE exe path to tmm_config.ini and closes window.
        '''
        # If tmm.ini doesn't exist, create it.
        if not os.path.exists('tmm.ini'):
            parser = ConfigParser()
            parser.add_section('Paths')
            with open(r'tmm.ini', 'w') as configfile:
                parser.write(configfile)

        # Save the exe path setting
        parser = ConfigParser()
        parser.read('tmm.ini')
        parser['Paths']['exepath'] = self.exe_path
        with open(r'tmm.ini', 'w') as configfile:
            parser.write(configfile)
        logging.info(f'Exe path set to {self.exe_path}')

        # If Settings opened via Launch button, launch on save
        if self.launch_on_save:
            self.launch_on_save = False
            self.launch_game()
        else:
            pass

        window.destroy()

    # === Toplevel Functions ===

    def open_settings(self):
        # Configure Window
        settings_win = Toplevel()
        settings_win.title('Trespasser Mod Manager - Settings')
        settings_win.resizable('False', 'False')
        self.parent.eval(f'tk::PlaceWindow {str(settings_win)} center')
        settings_win.grab_set()

        # Settings Window Labels
        settings_lbl = Label(
            settings_win,
            justify='left',
            wraplength=400,
            text='To launch Trespasser CE using Trespasser Mod Manager, find and save your Trespasser CE exe path below.'
        )
        settings_lbl.grid(column=0, row=0, columnspan=1, sticky='w', padx=10, pady=(10, 0))

        exepath_lbl = Label(settings_win, text='Trespasser CE exe path:')
        exepath_lbl.grid(column=0, row=1, sticky='w', padx=10, pady=(10, 0))

        exepath_field = Label(settings_win, justify='left', width=60, relief='sunken')
        exepath_field.grid(column=0, row=2, sticky='w', padx=(10, 0), pady=(5, 0))

        # If path already set, display path in field
        parser = ConfigParser()
        parser.read('tmm.ini')
        if parser.has_option('Paths', 'exepath'):
            exe_path = parser['Paths']['exepath']
            exepath_field.config(text=f'{exe_path}')

        # Settings Window Buttons
        exepath_btn = Button(
            settings_win,
            text='...',
            command=lambda: self.get_exepath(exepath_field)
        )
        exepath_btn.grid(column=1, row=2, padx=(5, 10))

        settings_savebtn = Button(
            settings_win,
            text='Save',
            command=lambda: self.save_settings(settings_win)
        )
        settings_savebtn.grid(column=3, row=3, sticky='se', padx=10, pady=10)

    # = Installation Functions =

    def install_mfz(self):
        '''
        Opens file browser for user selection of Tres CE exe path and installs.
        '''

        # Prompt user for zip file path

        zippath = filedialog.askopenfilename(
            initialdir='./',
            title='Select TMM-certified Mod Zip file',
            filetypes=[('TMM-certified Mod Zip file','*.zip')]
        )

        # Confirm that user selected a path

        if not zippath == '':

            # Get the fmpath to place the zip contents into

            fmpath = self.get_fmpath()

            with zipfile.ZipFile(zippath, 'r') as zip_file:
                zip_file.extractall(fmpath)

            # Notify user that installation was successful

            logging.info(f'Installed {zippath}')
            messagebox.showinfo(
                title='Trespasser Mod manager - Installation Complete!',
                message='Mod installed! Trespasser Mod Manager will now restart.'
            )

            # Restart TMM

            os.startfile('tmm.exe')
            raise SystemExit

    def install_retail(self):
        '''
        Installs the retail Trespasser game files from disc or folder.
        '''

        # Get the fmpath

        fmpath = self.get_fmpath()

        # Check to see if TrespasserRetail is already installed

        if os.path.isdir(f'{fmpath}/TrespasserRetail'):
            messagebox.showinfo(
                message='Trespasser has already been installed.'
                )
        else:
                
            # Promp user for Tres CD directory path

            cdpath = filedialog.askdirectory(
                initialdir='./',
                title='Select Trespasser CD directory'
            )

            # Confirm that user selected a path

            if not cdpath == '':

                # Create a list of all retail files

                retail_files = [
                    'as.GRF',
                    'as.scn',
                    'as.wtd',
                    'as2.grf',
                    'as2.scn',
                    'as2-130.pid',
                    'as2-130.spz',
                    'as2-130.swp',
                    'as4.wtd',
                    'as-130.pid',
                    'as-130.spz',
                    'as-130.swp',
                    'be.GRF',
                    'be.scn',
                    'be.wtd',
                    'be-130.pid',
                    'be-130.spz',
                    'be-130.swp',
                    'ij.GRF',
                    'ij.scn',
                    'ij.wtd',
                    'ij-130.pid',
                    'ij-130.spz',
                    'ij-130.swp',
                    'it.GRF',
                    'IT.scn',
                    'it.wtd',
                    'it-130.pid',
                    'it-130.spz',
                    'it-130.swp',
                    'jr.GRF',
                    'jr.scn',
                    'jr.wtd',
                    'jr-130.pid',
                    'jr-130.spz',
                    'jr-130.swp',
                    'lab.GRF',
                    'lab.scn',
                    'lab.wtd',
                    'lab-130.pid',
                    'lab-130.spz',
                    'lab-130.swp',
                    'sum.GRF',
                    'sum.scn',
                    'sum.wtd',
                    'sum-130.pid',
                    'sum-130.spz',
                    'sum-130.swp',
                    'testscene.GRF',
                    'TestScene.scn',
                    'testScene.wtd',
                    'TestScene-130.pid',
                    'TestScene-130.spz',
                    'TestScene-130.swp',
                    'testscnnght.GRF',
                    'TestScnNght.scn',
                    'TestScnNght-130.pid',
                    'TestScnNght-130.spz',
                    'TestScnNght-130.swp'
                ]

                # Create the folder to place the files
                os.makedirs(f'{fmpath}/TrespasserRetail')

                # Check the CD path for the files and copy them to the CE folder
                files = os.listdir(cdpath)
                for root, dirs, files in os.walk(cdpath):
                    for _file in files:
                        if _file in retail_files:
                            shutil.copy(os.path.abspath(root + '/' + _file), f'{fmpath}/TrespasserRetail')
                shutil.copytree(f'{cdpath}/data/menu', f'{fmpath}/TrespasserRetail/menu')

                # Create an info.txt for RetailTrespasser
                with open(f'{fmpath}/TrespasserRetail/info.txt', 'w') as f:
                    f.write('The original Trespasser experience by Dreamworks Interactive')

                # Notify user that installation was successful
                logging.info('Installed Trespasser')
                messagebox.showinfo(
                    title='Trespasser Mod Manager - Installation Complete!',
                    message='Trespasser installed! Trespasser Mod Manager will now restart.'
                )

                # Restart TMM
                os.startfile('tmm.exe')
                raise SystemExit


if __name__ == '__main__':
    validation()
    root = Tk()
    tmm_app = MainApplication(root)
    root.mainloop()