'''
dependency_validation
launch_game
get_installed_mods
ce_exe_settings_prompt
install_modfromzip_prompt
get_zip_path
install_modfromzip_prompt
'''

class Mod:
    def __init__(self, name, active=False, selected=False):
        self.name = name
        self.active = active
        self.selected = selected

    def get_name(self):
        return self.name

    def set_active(self, bool):
        self.active = bool

    def get_active(self):
        return self.active

    def set_selected(self, bool):
        self.selected = bool

    def get_selected(self):
        return self.selected

class TrespasserINI:
    def __init__(self, path='trespasser.ini'):
        self.path = path

    def get_path(self):
        return self.path

    def set_path(self, path):
        self.path = path

    def create_backup(self):
        pass

class CEOptionsSetting(TrespasserINI):
    def __init__(self):
        pass

    def set_bool(self, key, bool):
        pass

    def get_bool(self):
        pass

class TPModINI:
    def __init__(self, fmpath, quality, path='tp_mod.ini'):
        self.path = path
        self.quality = quality
        self.fmpath = fmpath

    def get_quality(self):
        return self.quality

    def set_quality(self, quality):
        self.quality = quality

    def get_fmpath(self):
        return self.fmpath

    def set_fmpath(self, path):
        self.fmpath = path

class ModManagerINI:
    def __init__(self, exe_path):
        self.exe_path = exe_path
        pass

    def create(self):
        pass

    def set_exe_path(self, exe_path):
        self.exe_path = exe_path

    def get_exe_path(self):
        return self.exe_path