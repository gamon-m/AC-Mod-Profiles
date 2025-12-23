# Introduction
ACMP (Assetto Corsa Mod Profiles) is a Python script that allows you to separate your modded tracks and cars from the main Assetto Corsa folder.

It also allows you to select different profiles, so that you if you have a lot of different mods you only need to select the ones you're going to use in that session. This should help with organizing your mods as well as performance when loading the game.

It works by creating symlinks (symbolic links) between each mod in your selected profile(s) and the Assetto Corsa directory. It automatically creates and removes these symlinks based on the selected profiles.


### *Important note:*

While this script should only delete symlinks that the script specifies, I am not responsible for any of your files being deleted. Do not manually change any of the json files and always backup your files.

## Installation
- Download the latest release from the releases page (acmp.zip)
- Extract into a new folder
- Run acmp.exe as administrator

## Usage
### *Note:*
Always run ampy.exe as administrator. Windows will not be able to create the symlinks if you do not. 

I would suggest to set the exe to always run as administrator by right clicking it > properties > compatibity tab > tick "run this program as administartor" > apply

### First startup and setup
Upon first startup you will be asked to enter the paths of your AC, tracks and cars folders.
I suggest to put your tracks and cars in a location separate from your Assetto installation.

For the Assetto Corsa path you want to select the root Assetto Corsa folder. 

Example:
`D:SteamLibrary\steamapps\common\assettocorsa\`


Your tracks and cars folders should include the profiles, and in each profile you should have the separate mods.

Mods need to be unzipped, exactly as they would be installed in the normal Assetto Corsa folder.

Example layout:
- tracks
    - track-profile 1
        - mod 1
        - mod 2
        - etc...
    - track-profile 2
        - mod 1
        - mod 2
        - etc...

(Same thing for cars)

### Main menu
Here you can chose if you want to select track profiles, car profiles or settings.

### Settings
If you set a path incorrectly, want to reset your config file, or remove all symlinks, you can do so from here.

Changing the Assetto Corsa path automatically removes all symlinks.

Changing the tracks or car paths will automatically reset the config for that type.

Reset config resets configs for both

### Car and track profiles
Use the arrow keys to move up and down, space to select a profile. You can also press a to select / deselect all profiles or i to invert your selection. Press enter to confirm the selection.

In the next section, if you didn't mean to make any changes you can select cancel, if you want to go back and change the selection you can select edit selection, or you can save the changes.

When you save the changes it will create and remove all required symlinks. If you get permission errors when saving profiles, restart the program as administrator, go to settings and select remove symlinks.

## Build
Before you can build the program yourself you will need a few prerequisites:
- Python >= 3.14: https://www.python.org/downloads/
- Poetry: https://python-poetry.org/docs/
- pyinstaller: https://pyinstaller.org/en/stable/

### Steps
1. Clone the repository or download source from latest release
2. Create a new terminal window from the repository (may need to run the terminal as administrator if you get issues installing dependencies)
3. Run "poetry install" to install dependencies
4. If you needed to run terminal as administrator, restart it as normal terminal in the same directory
5. Run "poetry env activate"
6. Run "poetry run pyinstaller acmp.py"

<br>

To remove the virtual environment(s) created by poetry:
1. Run "poetry env list"
2. Copy the active virtual environment or any you want to remove
3. Run "poetry env remove {environment_name}"

You should now see the built exe file in `project_root/dist/acmp`

You can open this file from this folder or move it wherever you like 

**Remember to always run as administartor!!!**

## Images
<img width="569" height="281" alt="acmp_WOV6vxOKtk" src="https://github.com/user-attachments/assets/12b7acbc-9058-421f-a824-b3abda907a31" />
<img width="569" height="281" alt="acmp_1zMwowDxLO" src="https://github.com/user-attachments/assets/ed640c6e-5fff-412b-a75c-050e11e7f8a7" />
<img width="569" height="281" alt="acmp_2Uplp6zqwu" src="https://github.com/user-attachments/assets/4df172e9-b666-4954-98ee-7e832275fcbd" />
<img width="569" height="281" alt="acmp_T3Y7LTA1Jq" src="https://github.com/user-attachments/assets/c61e1007-38c0-488e-989c-247b915c6c76" />
<img width="569" height="281" alt="acmp_fFFf3FKMcd" src="https://github.com/user-attachments/assets/36ef9524-a1a4-4010-98c1-1a8b5846c2fa" />
<img width="944" height="770" alt="explorer_9zGMB30mYN" src="https://github.com/user-attachments/assets/ce1ee3d0-ae64-44af-b14b-47c7f856399e" />
<img width="945" height="771" alt="firefox_AfhXQO9Y44" src="https://github.com/user-attachments/assets/0caaa922-db6d-4ab6-96a0-0c8b927383ef" />

