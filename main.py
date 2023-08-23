import curses
import webbrowser
import subprocess
from creator import *
import threading
import json
from os import system


# Define the states
STATE_MAIN_MENU = 0
STATE_HELP = 1
STATE_CREATE_RICH_PRESENCE = 2
STATE_SELECT_RICH_PRESENCE = 3

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
    
    stdscr.addstr(1, 0, "Press shift + ctrl + v to paste things. (*) mean this field is mandatory.")
    tutorial = rawInput(stdscr, 2, 0, "Do you want the tutorial? If yes write 'y' else press enter.")
    if(tutorial == "y"):
        createrpc_thread = threading.Thread(target=createInstructions)
        createrpc_thread.start()
    richPresenceName = rawInput(stdscr, 4, 0, "Name:")
    if(richPresenceName.decode() != ""):
        stdscr.addstr(5, 0, "> " + richPresenceName.decode() + " saved!")
        clientID = rawInput(stdscr, 6, 0, "Client ID (*):") 
        if(len(clientID.decode()) >= 17):
            stdscr.addstr(7, 0, "> " + clientID.decode() + " saved!")
            largeImageText = rawInput(stdscr, 8, 0, "Large Image Text:")
            stdscr.addstr(9, 0, "> " + largeImageText.decode() + " saved!")
            smallImageText = rawInput(stdscr, 10, 0, "Small Image Text:")
            stdscr.addstr(11, 0, "> " + smallImageText.decode() + " saved!")
            button1Name = rawInput(stdscr, 12, 0, "Button 1 Name:")
            stdscr.addstr(13, 0, "> " + button1Name.decode() + " saved!")
            button1URL = rawInput(stdscr, 14, 0, "Button 1 URL:")
            stdscr.addstr(15, 0, "> " + button1URL.decode() + " saved!")
            button2Name = rawInput(stdscr, 16, 0, "Button 2 Name:")
            stdscr.addstr(17, 0, "> " + button2Name.decode() + " saved!")
            button2URL = rawInput(stdscr, 18, 0, "Button 2 URL:")
            stdscr.addstr(19, 0, "> " + button2URL.decode() + " saved!")
            stateRPC = rawInput(stdscr, 20, 0, "State:")
            stdscr.addstr(21, 0, "> " + stateRPC.decode() + " saved!")
            details = rawInput(stdscr, 22, 0, "Details:")
            stdscr.addstr(23, 0, "> " + details.decode() + " saved!")
            saver = rawInput(stdscr, 24, 0, "PRESS ENTER TO SAVE")
                        
            settings_data[richPresenceName.decode()] = {  # Crée une nouvelle entrée avec le numéro trouvé
                "ClientID": clientID.decode(),
                "LargeImage": "large",
                "LargeImageText": largeImageText.decode(),
                "SmallImage": "small",
                "SmallImageText": smallImageText.decode(),
                "Button1": button1Name.decode(),
                "Url1": button1URL.decode(),
                "Button2": button2Name.decode(),
                "Url2": button2URL.decode(),
                "State": stateRPC.decode(),
                "Details": details.decode()
            }
            
            # Enregistrez les données mises à jour dans le fichier JSON
            with open("settings.json", "w") as json_file:
                json.dump(settings_data, json_file, indent=4)
            
            validation = rawInput(stdscr, 25, 0, "SAVE DONE, PRESS ENTER TO GO BACK TO THE MAIN MENU")
            state = STATE_MAIN_MENU
            
                    

        else:
            err = rawInput(stdscr, 6, 0, "PLEASE ENTER A CORRECT CLIENT ID. \n  PRESS ENTER TO RETURN BACK TO MAIN MENU.")
            state = STATE_MAIN_MENU
    else:
        err = rawInput(stdscr, 4, 0, "PLEASE ENTER A CORRECT NAME, AT LEAST ONE CHARACTER LONG. \n  PRESS ENTER TO RETURN BACK TO MAIN MENU")
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


def githubPage():
    webbrowser.open('https://github.com/Locox-dev/FlowCord')

def rawInput(stdscr, r, c, prompt_string):
    curses.echo() 
    stdscr.addstr(r, c, prompt_string)
    stdscr.addstr(r + 1, c, "> ")
    stdscr.refresh()
    input = stdscr.getstr(r + 1, c + 2, 20)
    return input

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

    # Create some UI elements
    ascii_title = read_ascii_title()
    menu_options = [
        ["Help", "Github Page", "Donate"],
        ["Create Rich Presence", "Select Rich Presence", "Delete Rich Presence"],
        ["Option 7", "Option 8", "Option 9"]
    ]
    current_column = 0
    current_row = 0
    current_row_select_rich_presence = 0
    
    back_button = [
        ["Back (Escape)"]
    ]
    
    with open("settings.json", "r") as json_file:
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

        if(richPresence == True):
            stdscr.addstr(0, 0, richPresenceName + " running.")


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
                # Now switch to a new state where you can handle the selected template/RPC
                #state = STATE_SELECT_RICH_PRESENCE
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
