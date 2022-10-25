# Trespasser Mod Manager
 A utility for managing mods in Trespasser CE.

The Trespasser Mod Manager (TMM) v0.3.1 performs the following functions:
    - Reads the tp_mod.ini to determine the Active Mod
    - Checks the contents of the /mods/ directory to generate a list of available mods
    - When prompted by the user, edits the tp_mod.ini to change the Active Mod
    - When prompted by the user, launches Trespasser CE (if using Trespasser 2020 distribution)

TMM v0.3.1 has the following known issues:
    - Lack of exception handling
    - Dependent on the presence of "/mods/" directory which can be named differently across various installations
    - Dependent on the presence of the Trespasser 2020 Tres CE exe for integrated game launch capability