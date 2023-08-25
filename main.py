import curses
import webbrowser
import subprocess
from creator import *
import threading
import json
from os import system
import os
import sys


# Define the states
STATE_MAIN_MENU = 0
STATE_HELP = 1
STATE_CREATE_RICH_PRESENCE = 2
STATE_SELECT_RICH_PRESENCE = 3
STATE_DELETE_RICH_PRESENCE = 4
STATE_CREATE_CUSTOM_CSS = 5

state = STATE_MAIN_MENU  # Initial state
richPresence = False
richPresenceName = ""

def read_ascii_title():
    with open("title.txt", "r", encoding="utf-8") as file:
        return file.read().splitlines()
    
def displayMainMenu(stdscr, ascii_title, menu_options, current_column, current_row):
    # Display ASCII art title
    title_height = len(ascii_title)
    title_left_margin = 2  # Position from the left margin
    for i, line in enumerate(ascii_title):
        stdscr.addstr(i + 1, title_left_margin, line, curses.A_BOLD)

    # Display menu options
    menu_top = title_height + 3  # Position of the first menu option
    menu_width_multiplicator = 30
    for row, options in enumerate(menu_options):
        if(row == 0):
            for col, option in enumerate(options):
                if col == current_column and row == current_row:
                    stdscr.addstr(menu_top + row, col * menu_width_multiplicator, f"> {option}", curses.color_pair(1) | curses.A_BOLD)
                else:
                    stdscr.addstr(menu_top + row, col * menu_width_multiplicator, f"  {option}")
                separator = "-" * (len(options) * menu_width_multiplicator)
                stdscr.addstr(menu_top + row + 1, 0, separator)
        if(row == 1):
            for col, option in enumerate(options):
                if col == current_column and row == current_row:
                    stdscr.addstr(menu_top + row + 1, col * menu_width_multiplicator, f"> {option}", curses.color_pair(1) | curses.A_BOLD)
                else:
                    stdscr.addstr(menu_top + row + 1, col * menu_width_multiplicator, f"  {option}")
        if(row == 2):
            for col, option in enumerate(options):
                if col == current_column and row == current_row:
                    stdscr.addstr(menu_top + row + 1, col * menu_width_multiplicator, f"> {option}", curses.color_pair(1) | curses.A_BOLD)
                else:
                    stdscr.addstr(menu_top + row + 1, col * menu_width_multiplicator, f"  {option}")

def displayHelp(stdscr, menu_options):
    stdscr.addstr(0, 0, "VERY LONG TEXT HERE")
    stdscr.addstr(10, 10, f"> {menu_options[0][0]}", curses.color_pair(1) | curses.A_BOLD)

def displayCreateRichPresence(stdscr, settings_data): # Always need to add something after an input or else it will all reset idk why
    global state
    
    stdscr.addstr(2, 0, "Press shift + ctrl + v to paste things. (*) mean this field is mandatory.")
    tutorial = rawInput(stdscr, 3, 0, "Do you want the tutorial? If yes write 'y' else press enter.")
    if(tutorial.decode().lower() == "y" or tutorial.decode().lower() == "yes"):
        createrpc_thread = threading.Thread(target=createInstructions)
        createrpc_thread.start()
    if(tutorial.decode() == "exit()"):
        state = STATE_MAIN_MENU
        return
    richPresenceName = rawInput(stdscr, 5, 0, "Name:")
    if(richPresenceName.decode() == "exit()"):
        state = STATE_MAIN_MENU
        return
    if(richPresenceName.decode() != ""):
        stdscr.addstr(6, 0, "> " + richPresenceName.decode() + " saved!")
        
        clientID = rawInput(stdscr, 7, 0, "Client ID (*):") 
        if(clientID.decode() == "exit()"):
            state = STATE_MAIN_MENU
            return
        if(len(clientID.decode()) >= 17):
            stdscr.addstr(8, 0, "> " + clientID.decode() + " saved!")
            
            largeImageName = rawInput(stdscr, 9, 0, "Large Image Name (default: large):")
            if(largeImageName.decode() == "exit()"):
                state = STATE_MAIN_MENU
                return
            largeImageNameReal = ""
            if(largeImageName.decode() == ""):
                largeImageNameReal = "large"
            else:
                largeImageNameReal = largeImageName.decode()
            stdscr.addstr(10, 0, "> " + largeImageNameReal + " saved!")
                
            largeImageText = rawInput(stdscr, 11, 0, "Large Image Text:")
            if(largeImageText.decode() == "exit()"):
                state = STATE_MAIN_MENU
                return
            if(largeImageText.decode() != "" and len(largeImageText.decode()) < 2):
                err = rawInput(stdscr, 12, 0, "Large Image Text should be at least 2 character long or none. \n  PRESS ENTER TO RETURN BACK TO MAIN MENU.")
                state = STATE_MAIN_MENU
            stdscr.addstr(12, 0, "> " + largeImageText.decode() + " saved!")
            
            smallImageName = rawInput(stdscr, 13, 0, "Small Image Name (default: small):")
            if(smallImageName.decode() == "exit()"):
                state = STATE_MAIN_MENU
                return
            smallImageNameReal = ""
            if(smallImageName.decode() == ""):
                smallImageNameReal = "small"
            else:
                smallImageNameReal = smallImageName.decode()
            stdscr.addstr(14, 0, "> " + smallImageNameReal + " saved!")
            
            smallImageText = rawInput(stdscr, 15, 0, "Small Image Text:")
            if(smallImageText.decode() == "exit()"):
                state = STATE_MAIN_MENU
                return
            if(smallImageText.decode() != "" and len(smallImageText.decode()) < 2):
                err = rawInput(stdscr, 16, 0, "Small Image Text should be at least 2 character long or none. \n  PRESS ENTER TO RETURN BACK TO MAIN MENU.")
                state = STATE_MAIN_MENU
            stdscr.addstr(16, 0, "> " + smallImageText.decode() + " saved!")
            
            button1Name = rawInput(stdscr, 17, 0, "Button 1 Name:")
            if(button1Name.decode() == "exit()"):
                state = STATE_MAIN_MENU
                return
            stdscr.addstr(18, 0, "> " + button1Name.decode() + " saved!")
            
            button1URL = rawInput(stdscr, 19, 0, "Button 1 URL:")
            if(button1URL.decode() == "exit()"):
                state = STATE_MAIN_MENU
                return
            stdscr.addstr(20, 0, "> " + button1URL.decode() + " saved!")
            
            button2Name = rawInput(stdscr, 21, 0, "Button 2 Name:")
            if(button2Name.decode() == "exit()"):
                state = STATE_MAIN_MENU
                return
            stdscr.addstr(22, 0, "> " + button2Name.decode() + " saved!")
            
            button2URL = rawInput(stdscr, 23, 0, "Button 2 URL:")
            if(button2URL.decode() == "exit()"):
                state = STATE_MAIN_MENU
                return
            stdscr.addstr(24, 0, "> " + button2URL.decode() + " saved!")
            
            stateRPC = rawInput(stdscr, 25, 0, "State:")
            if(stateRPC.decode() == "exit()"):
                state = STATE_MAIN_MENU
                return
            stdscr.addstr(26, 0, "> " + stateRPC.decode() + " saved!")
            
            details = rawInput(stdscr, 27, 0, "Details:")
            if(details.decode() == "exit()"):
                state = STATE_MAIN_MENU
                return
            stdscr.addstr(28, 0, "> " + details.decode() + " saved!")
            
            saver = rawInput(stdscr, 29, 0, "PRESS ENTER TO SAVE")
                        
            settings_data[richPresenceName.decode()] = {  # Crée une nouvelle entrée avec le numéro trouvé
                "ClientID": clientID.decode(),
                "LargeImage": largeImageNameReal,
                "LargeImageText": largeImageText.decode(),
                "SmallImage": smallImageNameReal,
                "SmallImageText": smallImageText.decode(),
                "Button1": button1Name.decode(),
                "Url1": button1URL.decode(),
                "Button2": button2Name.decode(),
                "Url2": button2URL.decode(),
                "State": stateRPC.decode(),
                "Details": details.decode()
            }
            
            # Enregistrez les données mises à jour dans le fichier JSON
            with open("richpresence.json", "w") as json_file:
                json.dump(settings_data, json_file, indent=4)
            
            validation = rawInput(stdscr, 30, 0, "SAVE DONE, PRESS ENTER TO GO BACK TO THE MAIN MENU")
            state = STATE_MAIN_MENU
            
                    

        else:
            err = rawInput(stdscr, 8, 0, "PLEASE ENTER A CORRECT CLIENT ID. \n  PRESS ENTER TO RETURN BACK TO MAIN MENU.")
            state = STATE_MAIN_MENU
    else:
        err = rawInput(stdscr, 6, 0, "PLEASE ENTER A CORRECT NAME, AT LEAST ONE CHARACTER LONG. \n  PRESS ENTER TO RETURN BACK TO MAIN MENU")
        state = STATE_MAIN_MENU

def displaySelectRichPresence(stdscr, settings_data, current_selection):
    stdscr.addstr(0, 0, "Select Rich Presence:")
    options = list(settings_data.keys())  # Get the keys (template/RPC names) from settings_data

    for i, option in enumerate(options):
        if i == current_selection:
            stdscr.addstr(i + 2, 0, f"> {option}", curses.color_pair(1) | curses.A_BOLD)
        else:
            stdscr.addstr(i + 2, 0, f"  {option}")

    stdscr.refresh()
    
def displayDeleteRichPresence(stdscr, settings_data, current_selection, deleteVerification):
    stdscr.addstr(0, 0, "Delete Rich Presence: \nPress enter to delete twice to delete the selected one.")
    options = list(settings_data.keys())  # Get the keys (template/RPC names) from settings_data

    for i, option in enumerate(options):
        if i == current_selection:
            stdscr.addstr(i + 3, 0, f"> {option}", curses.color_pair(1) | curses.A_BOLD)
        else:
            stdscr.addstr(i + 3, 0, f"  {option}")
            
    if(deleteVerification == True):
        stdscr.addstr(current_selection + 3, len(list(settings_data.keys())[current_selection]) + 5, "Press again to delete.", curses.color_pair(3))

    stdscr.refresh()
    
def displayCreateCustomCSS(stdscr):
    global state
    
    # Read the existing JSON data from customcss.json
    with open('customcss.json', 'r') as json_file:
        customcss_data = json.load(json_file)
    
    stdscr.addstr(2, 0, "Press shift + ctrl + v to paste things. (*) mean this field is mandatory.")
    name = rawInput(stdscr, 3, 0, "Custom CSS name: ")
    
    if(name.decode() == "exit()"):
        state = STATE_MAIN_MENU
        return
    
    if(name.decode() in customcss_data):
        stdscr.addstr(4, 0, f"Custom CSS name '{name.decode()}' already exists!")
    else:
        filename = name.decode().replace(" ", "_").lower() + ".css"
        stdscr.addstr(5, 0, f"Creating '{filename}'...")
        
        customcss_data[name.decode()] = filename
        with open('customcss.json', 'w') as json_file:
            json.dump(customcss_data, json_file, indent=4)
            
        # Create the CustomsCSS directory if it doesn't exist
        os.makedirs('CustomsCSS', exist_ok=True)
            
        css_file_path = os.path.abspath(f"CustomsCSS/{filename}")
        with open(css_file_path, 'w') as css_file:
            css_file.write("/* Your Custom CSS content here */")
            
        time.sleep(2) # Wait to be sure of the file creation
        
        stdscr.addstr(6, 0, f"Opening '{filename}'...")
        openDefaultEditor(css_file_path)
        
        rawInput(stdscr, 7, 0, f"Press enter to save your custom CSS.")
        validation = rawInput(stdscr, 9, 0, f"You can still modify it by going here {css_file_path}. Press enter to finish.")
        state = STATE_MAIN_MENU

def githubPage():
    webbrowser.open('https://github.com/Locox-dev/FlowCord')

def rawInput(stdscr, r, c, prompt_string):
    curses.echo() 
    stdscr.addstr(r, c, prompt_string)
    stdscr.addstr(r + 1, c, "> ")
    stdscr.refresh()
    input = stdscr.getstr(r + 1, c + 2, 20)
    return input

def openDefaultEditor(file_path):
    if sys.platform == "win32":
        os.startfile(file_path)
    elif sys.platform == "darwin":
        subprocess.run(["open", file_path])
    elif sys.platform.startswith("linux"):
        subprocess.run(["xdg-open", file_path])

def runRichPresence(selected):
    node_cmd = ["node", "node.js", selected]
    subprocess.run(node_cmd, text=True)

def main(stdscr):

    global state
    global richPresence
    global richPresenceName
    
    system('mode con: cols=120 lines=35') # Resize terminal window

    # Setup
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)   # Make getch() non-blocking
    curses.start_color()  # Enable color support
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Define a color pair (1)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Define a color pair (2)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)  # Define a color pair (3)

    # Create some UI elements
    ascii_title = read_ascii_title()
    menu_options = [
        ["Help", "Github Page", "Donate"],
        ["Create Rich Presence", "Select Rich Presence", "Delete Rich Presence"],
        ["Create Custom CSS", "Select Custom CSS", "Delete Custom CSS"] 
        # Create custom css = open text file in IDE and when saved it will be cloned into the discord-custom.css file
        # Create custom css = open text file in IDE and when saved it will be cloned into the discord-custom.css file
    ]
    current_column = 0
    current_row = 0
    current_row_select_rich_presence = 0
    current_row_delete_rich_presence = 0
    
    deleteVerification = False
    deleteVerificationRow = 10
    deleteVerificationColumn = 0
    deleteVerificationShow = False
    
    back_button = [
        ["Back (Escape)"]
    ]
    
    with open("richpresence.json", "r") as json_file:
        settings_data = json.load(json_file)

    while True:
        stdscr.clear()

        if(state == STATE_MAIN_MENU):
            displayMainMenu(stdscr, ascii_title, menu_options, current_column, current_row)
        elif(state == STATE_HELP):
            displayHelp(stdscr, back_button)
        elif(state == STATE_CREATE_RICH_PRESENCE):
            displayCreateRichPresence(stdscr, settings_data)
        elif(state == STATE_SELECT_RICH_PRESENCE):
            displaySelectRichPresence(stdscr, settings_data, current_row_select_rich_presence)
        elif(state == STATE_DELETE_RICH_PRESENCE):
            displayDeleteRichPresence(stdscr, settings_data, current_row_delete_rich_presence, deleteVerification)
        elif(state == STATE_CREATE_CUSTOM_CSS):
            displayCreateCustomCSS(stdscr)

        if(richPresence == True):
            stdscr.addstr(0, 0, richPresenceName + " running.", curses.color_pair(2))
            

        # Get user input
        key = stdscr.getch()

        # Handle ZQSD key presses in different states
        if(state == STATE_MAIN_MENU):
            if (key == ord('z') or key == curses.KEY_UP):  # Z key for moving up
                current_row = max(current_row - 1, 0)
            elif (key == ord('s') or key == curses.KEY_DOWN):  # S key for moving down
                current_row = min(current_row + 1, len(menu_options) - 1)
            elif (key == ord('q') or key == curses.KEY_LEFT):  # Q key for moving left
                current_column = max(current_column - 1, 0)
            elif (key == ord('d') or key == curses.KEY_RIGHT):  # D key for moving right
                current_column = min(current_column + 1, len(menu_options[0]) - 1)
            elif (key == ord('\n') or key == ord(' ')):
                # Perform some action based on the selected option
                selected_option = menu_options[current_row][current_column]

                if(selected_option == "Github Page"):
                    githubPage()
                if(selected_option == "Help"):
                    state = STATE_HELP
                if(selected_option == "Create Rich Presence"):
                    state = STATE_CREATE_RICH_PRESENCE
                if(selected_option == "Select Rich Presence"):
                    state = STATE_SELECT_RICH_PRESENCE
                if(selected_option == "Delete Rich Presence"):
                    state = STATE_DELETE_RICH_PRESENCE
                    deleteVerification = False
                if(selected_option == "Create Custom CSS"):
                    state = STATE_CREATE_CUSTOM_CSS
        elif(state == STATE_SELECT_RICH_PRESENCE):
            if (key == ord('z') or key == curses.KEY_UP):
                current_row_select_rich_presence = max(current_row_select_rich_presence - 1, 0)
            elif (key == ord('s') or key == curses.KEY_DOWN):
                current_row_select_rich_presence = min(current_row_select_rich_presence + 1, len(list(settings_data.keys())) - 1)
            elif (key == ord('\n') or key == ord(' ')):
                selected = list(settings_data.keys())[current_row_select_rich_presence]

                node_thread = threading.Thread(target=runRichPresence, args=(selected,))
                node_thread.start()

                state = STATE_MAIN_MENU
                richPresence = True
                richPresenceName = selected
        elif(state == STATE_DELETE_RICH_PRESENCE):
            if (key == ord('z') or key == curses.KEY_UP):
                current_row_delete_rich_presence = max(current_row_delete_rich_presence - 1, 0)
                deleteVerification = False
            elif (key == ord('s') or key == curses.KEY_DOWN):
                current_row_delete_rich_presence = min(current_row_delete_rich_presence + 1, len(list(settings_data.keys())) - 1)
                deleteVerification = False
            elif (key == ord('\n') or key == ord(' ')):
                selected = list(settings_data.keys())[current_row_delete_rich_presence]
                if(deleteVerification == False):
                    deleteVerification = True
                else:
                    if(selected in settings_data):
                        del settings_data[selected]

                    with open('richpresence.json', 'w') as json_file:
                        json.dump(settings_data, json_file, indent=4)
                        
                    deleteVerification = False
        elif(state == STATE_HELP):
            if (key == ord('\n') or key == ord(' ')):
                state = STATE_MAIN_MENU

        if key == 27:
            if(state == STATE_MAIN_MENU):
                exit()
            state = STATE_MAIN_MENU

        stdscr.refresh()

if __name__ == "__main__":
    curses.wrapper(main)
