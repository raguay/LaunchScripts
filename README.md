## LaunchScripts Plugin

Plugin for [fman.io](https://fman.io) that gives you the ability to launch scripts in a specified directory in the command pallet of fman. 

You can install this plugin by pressing `<shift+cmd+p>` to open the command pallet. Then type `install plugin`. Look for the `Launch Scripts` plugin and select it.

After restarting **fman**, you will have the ability to set a scripts directory, go to the scripts directory, and launch scripts from the scripts directory.

### Usage

Once loaded, use the `set script directory` command to set a directory where all your scripts will be placed. The default location is `~/bin`. Then use the other commands to interact with the scripts.

#### HotKeys Set

None set.

#### Commands

`go to scripts dir`
This command will open the current pane to the scripts directory.

`set show output`
This command will set the plug-in to show the output of running a script.

`set not show output`
This command will set the plug-in to not show the output of running a script.

`set script directory`
This command sets the currently highlighted directory as the script directory for running and creating scripts.

`launch script`
This command will run a script out of the script directory. A list of script files in the script directory will be presented to the user. Once selected, that script will be ran.

`edit script`
This command will allow the user to edit the script selected. A list of scripts in the scripts directory will be presented to the user to choose from. Once selected, the `open with editor` command will be used to edit the file.

`create script`
This command will ask for a script name. If a file or directory doesn't exist with that name, it will be created, a base script template will be written to it, the execution bit will be set, and the `open with editor` command will be called to edit the newly created script.

#### Files Created and Used

New script files will be created in the user specified scripts directory when the `create script` command is issued.

The plugin will create the following environment variables for the scripts to use:

$FILES_SELECTED - The currently selected file

$LEFT_PANE - The directory of the left pane

$RIGHT_PANE - The directory of the right pane

$CURRENT_DIRECTORY - The currently selected directory

$LEFT_PANE_SELECTED_FILE - The currently selected file in the left pane

$RIGHT_PANE_SELECTED_FILE - The currently selected file in the right pane

### Features

- Set a scripts directory to store scripts.
- Launch scripts from the script directory.
- Edit scripts in the scripts directory.
- Create new scripts in the scripts directory.
