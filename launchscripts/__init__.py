#
# Load the libraries that are used in these commands.
#
from core.quicksearch_matchers import contains_chars
from fman import DirectoryPaneCommand, show_prompt, show_quicksearch, QuicksearchItem, show_status_message, clear_status_message, save_json, load_json, show_alert
import os
import re
from fman.url import as_human_readable
from fman.url import as_url
from subprocess import run, PIPE

#
# Function:       _GetScriptVars
#
# Description:    This function gets the variables for this
#                 plugin.
#
def _GetScriptVars():
    #
    # Get the scripts directory.
    #
    scriptVars = load_json("LaunchScript.json")
    if scriptVars is None:
        scriptVars = dict()
        scriptVars['show_output'] = True
        scriptVars['directory'] = '~/bin'
        save_json("LaunchScript.json", scriptVars)
    return(scriptVars)

#
# Function:    _SaveScriptVars
#
# Description: This function saves a new set of variables
#              for this plugin.
#
def _SaveScriptVars(scriptVars):
    save_json("LaunchScript.json", scriptVars)

#
# Function:    GoToScriptsDir
#
# Description: This class performs the operation of going
#              to the scripts directory.
#
class GoToScriptsDir(DirectoryPaneCommand):
    #
    # This directory command is for showing the scripts
    # directory in the current Directory Pane.
    #
    def __call__(self):
        scriptDir = _GetScriptVars()
        self.pane.set_path(as_url(os.path.expanduser(scriptDir['directory'] + os.sep)))

#
# Function:   SetShowOutput
#
# Description: This function sets the flag to show
#              the output of the script.
#
class SetShowOutput(DirectoryPaneCommand):
    def __call__(self):
        scriptVars = _GetScriptVars()
        scriptVars['show_output'] = True
        _SaveScriptVars(scriptVars)

#
# Function:   SetNotShowOutput
#
# Description: This function sets the flag to not show
#              the output of the script.
#
class SetNotShowOutput(DirectoryPaneCommand):
    def __call__(self):
        scriptVars = _GetScriptVars()
        scriptVars['show_output'] = False
        _SaveScriptVars(scriptVars)

#
# Function:   SetTheScriptsDirectory(DirectoryPaneCommand)
#
# Description: This class performs the function of
#              setting the Scripts Directory location.
#
class SetTheScriptsDirectory(DirectoryPaneCommand):
    #
    # This directory command is for setting the
    # Scripts Directory location.
    #
    def __call__(self):
        show_status_message('Setting the Scripts Directory')
        selected_files = self.pane.get_selected_files()
        if len(selected_files) >= 1 or (len(selected_files) == 0 and self.get_chosen_files()):
            if len(selected_files) == 0 and self.get_chosen_files():
                selected_files.append(self.get_chosen_files()[0])
            dirName = as_human_readable(selected_files[0])
            if os.path.isfile(dirName):
                #
                # It's a file, not a directory. Get the directory
                # name for this file's parent directory.
                #
                dirName = os.path.dirname(dirName)
            scriptDir = _GetScriptVars()
            scriptDir['directory'] = dirName
            _SaveScriptVars(scriptDir)
        else:
            show_alert("Directory not selected.")
        clear_status_message()

#
# Function:    LaunchScript
#
# Description: This class performs the function of
#              launching a script from the scripts
#              directory.
#
class LaunchScript(DirectoryPaneCommand):
    #
    # This directory command is for launching
    # a selected script.
    #
    def __call__(self):
        show_status_message('Launching a Script...')
        result = show_quicksearch(self._suggest_script)
        if result:
            #
            # Launch the script given. Show the output.
            #
            query, script = result

            #
            # Get the variables for this plugin
            #
            scriptVars = _GetScriptVars()

            #
            # Get a list of selected files.
            #
            selected_files = self.pane.get_selected_files()
            if len(selected_files) >= 1 or (len(selected_files) == 0 and self.get_chosen_files()):
                if len(selected_files) == 0 and self.get_chosen_files():
                    selected_files.append(self.get_chosen_files()[0])
            fileList = ''
            first = True
            for file in selected_files:
                if first:
                    fileList += as_human_readable(file)
                else:
                    fileList += ',' + as_human_readable(file)

            #
            # Set the environment variables for the scripts to use.
            #
            os.putenv('CURRENT_DIRECTORY', as_human_readable(self.pane.get_path()))
            panes = self.pane.window.get_panes()
            os.putenv('LEFT_PANE', as_human_readable(panes[0].get_path()))
            os.putenv('LEFT_PANE_SELECTED_FILE',as_human_readable(panes[0].get_file_under_cursor()))
            os.putenv('RIGHT_PANE', as_human_readable(panes[1].get_path()))
            os.putenv('RIGHT_PANE_SELECTED_FILE',as_human_readable(panes[1].get_file_under_cursor()))
            os.putenv('FILES_SELECTED',fileList)

            #
            # Run the script.
            #
            Output = run("'" + scriptVars['directory'] + "/" + script + "'",stdout=PIPE,shell=True)
            if scriptVars['show_output']:
                show_alert(Output.stdout.decode("utf-8"))
        clear_status_message()

    def _suggest_script(self, query):
        scripts = ["No scripts are setup."]
        #
        # Get a list of scripts.
        #
        scriptDir = _GetScriptVars()
        scripts = os.listdir(scriptDir['directory'])

        #
        # Suggested one to the user and let them pick.
        #
        for script in scripts:
            if script.strip() != "":
                scriptName = script
                match = contains_chars(scriptName.lower(), query.lower())
                if match or not query:
                    yield QuicksearchItem(scriptName, highlight=match)

#
# Function:    EditScript
#
# Description: This class performs the function of
#              editing a script from the scripts
#              directory.
#
class EditScript(DirectoryPaneCommand):
    #
    # This directory command is for launching
    # a selected script.
    #
    def __call__(self):
        show_status_message('Editing a Script...')
        result = show_quicksearch(self._suggest_script)
        if result:
            #
            # Launch the script given. Show the output.
            #
            query, script = result

            #
            # Get the variables for this plugin
            #
            scriptVars = _GetScriptVars()

            #
            # Edit the script file.
            #
            if self.pane.is_command_visible('open_with_editor'):
                self.pane.run_command('open_with_editor',{'url': as_url(scriptVars['directory'] + os.sep + script)})
            else:
                show_alert("OpenWithEditor command not found.")
        clear_status_message()

    def _suggest_script(self, query):
        scripts = ["No scripts are setup."]
        #
        # Get a list of scripts.
        #
        scriptDir = _GetScriptVars()
        scripts = os.listdir(scriptDir['directory'])

        #
        # Suggested one to the user and let them pick.
        #
        for script in scripts:
            if script.strip() != "":
                scriptName = script
                match = contains_chars(scriptName.lower(), query.lower())
                if match or not query:
                    yield QuicksearchItem(scriptName, highlight=match)

#
# Function:    CreateScript
#
# Description: This class performs the function of
#              creating a script and then editing the newly
#              created script from the scripts
#              directory.
#
class CreateScript(DirectoryPaneCommand):
    #
    # This directory command is for launching
    # a selected script.
    #
    def __call__(self):
        show_status_message('Creating a Script...')
        scriptVars = _GetScriptVars()
        script, flags = show_prompt("New Script Name?")
        newScript = scriptVars['directory'] + os.sep + script
        if os.path.isdir(newScript):
            show_alert("This is a directory.")
        else:
            if os.path.isfile(newScript):
                show_alert("Script already exists.")
            else:
                #
                # Create the script file.
                #
                fp = open(newScript,"w+")
                fp.write("#!/bin/sh\n\n")
                fp.write("#\n# The following variable are usable:\n#\n")
                fp.write("# $FILES_SELECTED - The currently selected file\n")
                fp.write("# $LEFT_PANE - The directory of the left pane\n")
                fp.write("# $RIGHT_PANE - The directory of the right pane\n")
                fp.write("# $CURRENT_DIRECTORY - The currently selected directory\n")
                fp.write("# $LEFT_PANE_SELECTED_FILE - The currently selected file in the left pane\n")
                fp.write("# $RIGHT_PANE_SELECTED_FILE - The currently selected file in the right pane\n")
                fp.close()
                os.chmod(newScript,0o755)

                #
                # Edit the script file.
                #
                if self.pane.is_command_visible('open_with_editor'):
                    self.pane.run_command('open_with_editor',{'url': as_url(newScript)})
        clear_status_message()
