import curses
import webbrowser
from creator import *
import time
import json


# Define the states
STATE_MAIN_MENU = 0
STATE_HELP = 1
STATE_CREATE_RICH_PRESENCE = 2

state = STATE_MAIN_MENU  # Initial state

def read_ascii_title():
    with open("title.txt", "r", encoding="utf-8") as file:
        return file.read().splitlines()
    
def displayMainMenu(stdscr, ascii_title, menu_options, current_column, current_row):
    # Display ASCII art title
    title_height = len(ascii_title)
    title_left_margin = 2  # Position from the left margin
    for i, line in enumerate(ascii_title):
        stdscr.addstr(i, title_left_margin, line, curses.A_BOLD)

    # Display menu options
    menu_top = title_height + 2  # Position of the first menu option
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
    
    richPresenceName = rawInput(stdscr, 1, 0, "Name:")
    if(richPresenceName.decode() != ""):
        stdscr.addstr(2, 0, "> " + richPresenceName.decode() + " saved!")
        clientID = rawInput(stdscr, 3, 0, "Client ID:") 
        if(len(clientID.decode()) >= 17):
            stdscr.addstr(4, 0, "> " + clientID.decode() + " saved!")
            largeImageText = rawInput(stdscr, 5, 0, "Large Image Text:")
            if(largeImageText != ""):
                stdscr.addstr(6, 0, "> " + largeImageText.decode() + " saved!")
                
                
                settings_data[richPresenceName.decode()] = {  # Crée une nouvelle entrée avec le numéro trouvé
                    "ClientID": clientID.decode(),
                    "LargeImage": "large",
                    "LargeImageText": largeImageText.decode(),
                    "SmallImage": "",
                    "SmallImageText": "",
                    "Button1": "",
                    "Url1": "",
                    "Button2": "",
                    "Url2": "",
                    "State": "",
                    "Details": ""
                }
                
                # Enregistrez les données mises à jour dans le fichier JSON
                with open("settings.json", "w") as json_file:
                    json.dump(settings_data, json_file, indent=4)
                    
                smallImageText = rawInput(stdscr, 7, 0, "Small Image Text:")
        else:
            err = rawInput(stdscr, 3, 0, "PLEASE ENTER A CORRECT CLIENT ID. \n  PRESS ENTER TO RETURN BACK TO MAIN MENU.")
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

def main(stdscr):

    global state

    # Setup
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)   # Make getch() non-blocking
    curses.start_color()  # Enable color support
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Define a color pair (1)

    # Create some UI elements
    ascii_title = read_ascii_title()
    menu_options = [
        ["Help", "Github Page", "Donate"],
        ["Create Rich Presence", "Enable Rich Presence", "Delete Rich Presence"],
        ["Option 7", "Option 8", "Option 9"]
    ]
    current_column = 0
    current_row = 0
    
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



        # Get user input
        key = stdscr.getch()

        # Handle ZQSD key presses in different states
        if(state == STATE_MAIN_MENU):
            if key == ord('z'):  # Z key for moving up
                current_row = max(current_row - 1, 0)
            elif key == ord('s'):  # S key for moving down
                current_row = min(current_row + 1, len(menu_options) - 1)
            elif key == ord('q'):  # Q key for moving left
                current_column = max(current_column - 1, 0)
            elif key == ord('d'):  # D key for moving right
                current_column = min(current_column + 1, len(menu_options[0]) - 1)
            elif key == ord('\n') or key == ord(' '):
                # Perform some action based on the selected option
                selected_option = menu_options[current_row][current_column]

                if(selected_option == "Github Page"):
                    githubPage()
                if(selected_option == "Help"):
                    state = STATE_HELP
                if(selected_option == "Create Rich Presence"):
                    state = STATE_CREATE_RICH_PRESENCE
                    #createInstructions()
        elif(state == STATE_HELP):
            if key == ord('\n') or key == ord(' '):
                state = STATE_MAIN_MENU
        elif(state == STATE_CREATE_RICH_PRESENCE):
            if key == 27:
                state = STATE_MAIN_MENU

        stdscr.refresh()

if __name__ == "__main__":
    curses.wrapper(main)
