## LaunchScripts Plugin

Plugin for [fman.io](https://fman.io) that gives you the ability to launch scripts in a specified directory in the command pallet of fman. 

You can install this plugin by pressing `<shift+cmd+p>` to open the command pallet. Then type `install plugin`. Look for the `Launch Scripts` plugin and select it.

After restarting **fman**, you will have the ability to set a scripts directory, go to the scripts directory, and launch scripts from the scripts directory.

### Usage

Once loaded, use the `set script directory` command to set a directory where all your scripts will be placed. The default location is `~/bin`. Then use the other commands to interact with the scripts.

Then use the `set shell script` command to set your shell's initializing script. You can give it `~/.zshrc` and it will expand out the home directory okay. This is used to keep a consistant environment when executing scripts. It is necessary to properly run the `launch npm script` command.

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

`set shell script`
This command allows the user to tell the plugin what script is their shell's initializing script. You can give it `~/.zshrc` and it will expand it to the absolute path. This is used to setup the proper environment for running the scripts.

`launch script`
This command will run a script out of the script directory. A list of script files in the script directory will be presented to the user. Once selected, that script will be ran.

`edit script`
This command will allow the user to edit the script selected. A list of scripts in the scripts directory will be presented to the user to choose from. Once selected, the `open with editor` command will be used to edit the file.

`create script`
This command will ask for a script name. If a file or directory doesn't exist with that name, it will be created, a base script template will be written to it, the execution bit will be set, and the `open with editor` command will be called to edit the newly created script.

`launch npm script`
This command will list all the npm scripts listed in the current directory's package.json file. It will then run the script the user selects from that list.

`run command line`
This command will prompt the user for a command line string. That string will be ran and the results display if the `set show output` is set. These command lines can use the following environment variables:

$cd - The current directory

$lp - The left panel directory

$lpf - The left panel file

$rp - The right panel directory

$rpf - The right panel file

$cf - The current file under the cursor of the current panel. The path is removed and is just the file name. Since the directory is moved to before running the command, this makes for an easy way to reference the current file without worrying about special characters in the path (like spaces).

The commands are sorted and similar command lines are removed to compact the history. Therefore, you can run the same command many times, but it will be in the history only once. Unfortunately, this doesn't preserve the order of command execution.

If you are using a full path environment variable, you will want to reference it like this:  `ls "${cd}"`. This will list the current directory with preserving the file path spaces. But, since the current directory is moved to before running the command, you can just use `ls`. This is just to illustrate the issue.

#### Files Created and Used

New script files will be created in the user specified scripts directory when the `create script` command is issued.

The plugin will create the following environment variables for the scripts to use:

$FILES_SELECTED - The currently selected file

$LEFT_PANE - The directory of the left pane

$RIGHT_PANE - The directory of the right pane

$CURRENT_DIRECTORY - The currently selected directory

$LEFT_PANE_SELECTED_FILE - The currently selected file in the left pane

$RIGHT_PANE_SELECTED_FILE - The currently selected file in the right pane

### Example Scripts

I created another [repository](https://github.com/raguay/fman-Launch-Script-Scripts) of scripts that I use with this plugin. Give them a try and add your own!

### Features

- Set a scripts directory to store scripts.
- Launch scripts from the script directory.
- Edit scripts in the scripts directory.
- Create new scripts in the scripts directory.
- Launch a NPM script in a directory with a `package.json` file.
- Set the shell initializing script to setup the environment properly.
- Currently, only tested under macOS.
- Run a command line and save them in a history buffer.

### Features Still in the Works

- Run Gulp commands
