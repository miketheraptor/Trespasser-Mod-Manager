# About The Project

**Trespasser Mod Manager (TMM)**

*The GUI-based utility for managing Trespasser mods.*

<p float="left">
 <img width="357" alt="Trespasser CE v1.0.0 Mods Tab" src="https://user-images.githubusercontent.com/18666598/211119258-7a76b83f-e1b0-44f1-b17e-025854ad9198.png">
 <img width="357" alt="Trespasser CE v1.0.0 CE Options Tab" src="https://user-images.githubusercontent.com/18666598/211119273-0f9635b7-b947-4091-9d06-33acb15a9b1a.png">
</p>

# Getting Started

## Prerequisites
* Trespasser CE

Trespasser CE is an unofficial patch for the Trespasser engine which adds DirectX9 support, enhanced mod support, and various other bug fixes and features which increase graphical fidelity, frame rates, and overall stability.

Trespasser Mod Manager is dependant on features introduced by Trespasser CE.

### How to Download Trespasser CE

#### Easy Method (Trespasser 2020)
Trespasser 2020 contains a prepackaged, standalone version of the Trespasser CE engine that can run Trespasser levels and mods without needing the retail game.
1. [Download Trespasser 2020](https://www.trescom.org/download/trespasser-2020-a-trespasser-modding-starter-kit/) from TresCom.
2. Extract the contents of the 7z archive to your PC.

#### Advanced Method (Manually Patch a Retail Installation)
The retail game engine can be manually patched.
1. [Download Trespasser CE Patch](https://www.trescom.org/download/trespasser-ce-patch/) from TresCom.
2. Extract the contents of the tpass-ce.zip and contrib.zip archives to your Trespasser installation folder.
3. Copy and paste the tp_mod.ini file from the /doc/ folder to the installation folder (same folder as Trespasser exe file).
4. Create a new folder in the installation folder (same folder as Trespasser exe file) for storing your mods. The folder can be named anything, but the default for Trespasser CE is /FMs/
5. Edit the tp_mod.ini folder and remove the ";" from the line `;FMPath=FMs`. FMs refers to your mods folder and it can be changed if you used a different name. Example: `FMPath=mods`.
6. Copy and paste the trespasser_dx9.ini or trespasser_dx9-hq.ini from the /doc/configs/ folder to the installation folder (same folder as Trespasser exe file). This file controls some Trespasser CE settings. The hq file has higher graphics settings but can be less stable.

## Installation
1. Check [releases](https://github.com/miketheraptor/Trespasser-Mod-Manager/releases) for the latest version of Trespasser Mod Manager and download it.
2. Place the tmm.exe file into the Trespasser CE directory (the same folder where the Trespasser CE exe is located).

# Usage
Trespasser Mod Manager can be used to do the following:
* Set the active Trespasser mod
* Read descriptions for installed mods that support the feature
* Toggle Trespasser CE settings
* Install a "TMM certified" Trespasser mod
* Install the retail level files to your Trespasser CE installation from a CD/iso/folder containing the files
* Launch Trespasser CE

# For Trespasser Modders / Level Creators
This section is for people who are creating new content for Trespasser. Trespasser Mod Manager includes some modding features you might like to take advantage of.

## Mod Description File (info.txt)
Trespasser Mod Manager checks installed mods for the presence of a file named "info.txt". Any text placed into the "info.txt" file will be displayed in the Mod Description textbox when the mod is selected.

Place the "info.txt" file into the mod's top folder. An example path could be: TresCE/mods/YourMod/info.txt. In this example, TresCE is the folder containing the tmm.exe and Trespasser CE .exe files, mods is the fmpath, and YourMod is the folder containing all of your mod's files.

## Making Mods Compatible with TMM Install Mod from Zip Feature (TMM Certified Mods)
TMM Certified Mods are mods which are standardized for compatability with Trespasser Mod Manager's Install Mod from Zip functionality. This makes it easy for players to install your mod without having to read a readme file or manually place folders and files in specific directories.

In order to be compatible, follow these guidelines:
* Use a .zip archive to store all of the levels. Other popular archives (7z, rar) are not supported
* Inside the .zip archive, all levels should be stored in a mod folder named for your mod. TMM will extract this folder and place it inside the player's fmpath directory. The name of this folder will appear in the mods list in TMM.
* All other mod files should be inside the mod folder.

# Acknowledgements
Thank you to the members at the TresCom Discord and Forum whose support and suggestions fueled this project's development.

Join the Trespasser Community at TresCom by following the links below:
* [TresCom Forum](https://www.trescom.org)
* [TresCom Discord](https://discord.gg/xHmu7cF7v4)
