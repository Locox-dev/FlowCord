import curses
import webbrowser
import subprocess
from creator import *
import threading
import json
from os import system
import os
import sys
import platform


# Define the states
STATE_MAIN_MENU = 0
STATE_HELP = 1
STATE_CREATE_RICH_PRESENCE = 2
STATE_SELECT_RICH_PRESENCE = 3
STATE_DELETE_RICH_PRESENCE = 4
STATE_CREATE_CUSTOM_CSS = 5
STATE_SELECT_CUSTOM_CSS = 6
STATE_DELETE_CUSTOM_CSS = 7

state = STATE_MAIN_MENU  # Initial state

richPresence = False
richPresenceName = ""

customCSS = False
customCSSName = ""

terminal_width = 120
terminal_height = 35

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
    stdscr.addstr(0, 4, """HELP GUIDE \n
    You can type `exit()` in any text inputs to go back to the main menu. \n
    You can press the Escape key to go back to the main menu (except in inputs). \n
    Do not use `ctrl + shift + del` to delete a full world, this will bug the input. \n
    Use `ctrl + shift + c` and `ctrl + shift + v` to copy and paste things.""")
    stdscr.addstr(10, 10, f"> {menu_options[0][0]}", curses.color_pair(1) | curses.A_BOLD)

def displayCreateRichPresence(stdscr, richpresence_data): # Always need to add something after an input or else it will all reset idk why
    global state
    
    stdscr.addstr(2, 0, "Press shift + ctrl + v to paste things. Enter 'exit()' to quit the creation process.")
    tutorial = rawInput(stdscr, 3, 0, "Do you want the tutorial? If yes write 'y' else press enter.")
    if(tutorial.decode().lower() == "y" or tutorial.decode().lower() == "yes"):
        createrpc_thread = threading.Thread(target=createInstructions)
        createrpc_thread.start()
    if(isItExit(tutorial.decode())): return
    richPresenceName = rawInput(stdscr, 5, 0, "Name:")
    if(isItExit(richPresenceName.decode())): return
    if(richPresenceName.decode() != ""):
        stdscr.addstr(6, 0, "> " + richPresenceName.decode() + " saved!")
        
        clientID = rawInput(stdscr, 7, 0, "Client ID:") 
        if(isItExit(clientID.decode())): return
        if(len(clientID.decode()) >= 17):
            stdscr.addstr(8, 0, "> " + clientID.decode() + " saved!")
            
            largeImageName = rawInput(stdscr, 9, 0, "Large Image Name (default: large):")
            if(isItExit(largeImageName.decode())): return
            largeImageNameReal = ""
            if(largeImageName.decode() == ""):
                largeImageNameReal = "large"
            else:
                largeImageNameReal = largeImageName.decode()
            stdscr.addstr(10, 0, "> " + largeImageNameReal + " saved!")
                
            largeImageText = rawInput(stdscr, 11, 0, "Large Image Text:")
            if(isItExit(largeImageText.decode())): return
            if(largeImageText.decode() != "" and len(largeImageText.decode()) < 2):
                err = rawInput(stdscr, 12, 0, "Large Image Text should be at least 2 character long or none. \n  PRESS ENTER TO RETURN BACK TO MAIN MENU.")
                state = STATE_MAIN_MENU
            stdscr.addstr(12, 0, "> " + largeImageText.decode() + " saved!")
            
            smallImageName = rawInput(stdscr, 13, 0, "Small Image Name (default: small):")
            if(isItExit(smallImageName.decode())): return
            smallImageNameReal = ""
            if(smallImageName.decode() == ""):
                smallImageNameReal = "small"
            else:
                smallImageNameReal = smallImageName.decode()
            stdscr.addstr(14, 0, "> " + smallImageNameReal + " saved!")
            
            smallImageText = rawInput(stdscr, 15, 0, "Small Image Text:")
            if(isItExit(smallImageText.decode())): return
            if(smallImageText.decode() != "" and len(smallImageText.decode()) < 2):
                err = rawInput(stdscr, 16, 0, "Small Image Text should be at least 2 character long or none. \n  PRESS ENTER TO RETURN BACK TO MAIN MENU.")
                state = STATE_MAIN_MENU
            stdscr.addstr(16, 0, "> " + smallImageText.decode() + " saved!")
            
            button1Name = rawInput(stdscr, 17, 0, "Button 1 Name:")
            if(isItExit(button1Name.decode())): return
            stdscr.addstr(18, 0, "> " + button1Name.decode() + " saved!")
            
            button1URL = rawInput(stdscr, 19, 0, "Button 1 URL:")
            if(isItExit(button1URL.decode())): return
            stdscr.addstr(20, 0, "> " + button1URL.decode() + " saved!")
            
            button2Name = rawInput(stdscr, 21, 0, "Button 2 Name:")
            if(isItExit(button2Name.decode())): return
            stdscr.addstr(22, 0, "> " + button2Name.decode() + " saved!")
            
            button2URL = rawInput(stdscr, 23, 0, "Button 2 URL:")
            if(isItExit(button2URL.decode())): return
            stdscr.addstr(24, 0, "> " + button2URL.decode() + " saved!")
            
            stateRPC = rawInput(stdscr, 25, 0, "State:")
            if(isItExit(stateRPC.decode())): return
            stdscr.addstr(26, 0, "> " + stateRPC.decode() + " saved!")
            
            details = rawInput(stdscr, 27, 0, "Details:")
            if(isItExit(details.decode())): return
            stdscr.addstr(28, 0, "> " + details.decode() + " saved!")
            
            saver = rawInput(stdscr, 29, 0, "PRESS ENTER TO SAVE")
            if(isItExit(saver.decode())): return
                        
            richpresence_data[richPresenceName.decode()] = {  # Crée une nouvelle entrée avec le numéro trouvé
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
            with open("JSON/richpresence.json", "w") as json_file:
                json.dump(richpresence_data, json_file, indent=4)
            
            validation = rawInput(stdscr, 30, 0, "SAVE DONE, PRESS ENTER TO GO BACK TO THE MAIN MENU")
            state = STATE_MAIN_MENU
            
                    

        else:
            err = rawInput(stdscr, 8, 0, "PLEASE ENTER A CORRECT CLIENT ID. \n  PRESS ENTER TO RETURN BACK TO MAIN MENU.")
            state = STATE_MAIN_MENU
    else:
        err = rawInput(stdscr, 6, 0, "PLEASE ENTER A CORRECT NAME, AT LEAST ONE CHARACTER LONG. \n  PRESS ENTER TO RETURN BACK TO MAIN MENU")
        state = STATE_MAIN_MENU

def displaySelectRichPresence(stdscr, richpresence_data, current_selection):
    stdscr.addstr(0, 0, "Select Rich Presence:")
    keys = list(richpresence_data.keys())

    for i, key in enumerate(keys):
        if i == current_selection:
            stdscr.addstr(i + 2, 0, f"> {key}", curses.color_pair(1) | curses.A_BOLD)
        else:
            stdscr.addstr(i + 2, 0, f"  {key}")

    stdscr.refresh()
    
def displayDeleteRichPresence(stdscr, richpresence_data, current_selection, deleteVerification):
    stdscr.addstr(0, 0, "Delete Rich Presence: \nPress enter twice to delete the selected one.")
    keys = list(richpresence_data.keys())

    for i, key in enumerate(keys):
        if i == current_selection:
            stdscr.addstr(i + 3, 0, f"> {key}", curses.color_pair(1) | curses.A_BOLD)
        else:
            stdscr.addstr(i + 3, 0, f"  {key}")
            
    if(deleteVerification == True):
        stdscr.addstr(current_selection + 3, len(list(richpresence_data.keys())[current_selection]) + 5, "Press again to delete.", curses.color_pair(3))

    stdscr.refresh()
    
def displayCreateCustomCSS(stdscr, customcss_data):
    global state
    
    stdscr.addstr(2, 0, "Press shift + ctrl + v to paste things. Enter 'exit()' to quit the creation process.")
    name = rawInput(stdscr, 3, 0, "Custom CSS name: ")
    
    if(isItExit(name.decode())): return
    if(name.decode().lower() == "revert"):
        rawInput(stdscr, 5, 0, "You can't name it 'revert', PRESS ENTER TO GO BACK TO MAIN MENU.")
        state = STATE_MAIN_MENU
        return
    if(name.decode().lower() == "disable"):
        rawInput(stdscr, 5, 0, "You can't name it 'disable', PRESS ENTER TO GO BACK TO MAIN MENU.")
        state = STATE_MAIN_MENU
        return
    
    if(name.decode() in customcss_data):
        rawInput(stdscr, 4, 0, f"Custom CSS name '{name.decode()}' already exists! PRESS ENTER TO GO BACK TO MAIN MENU.")
        state = STATE_MAIN_MENU
        return
    else:
        filename = name.decode().replace(" ", "_").lower() + ".css"
        stdscr.addstr(5, 0, f"Creating '{filename}'...")
        
        # Create the CustomsCSS directory if it doesn't exist
        os.makedirs('CustomsCSS', exist_ok=True)
        
        css_file_path = os.path.abspath(f"CustomsCSS/{filename}")
        customcss_data[name.decode()] = css_file_path
        with open('JSON/customcss.json', 'w') as json_file:
            json.dump(customcss_data, json_file, indent=4)
        
        with open(css_file_path, 'w') as css_file:
            css_file.write("/* Your Custom CSS content here */\n/* You can also find CSS files here: https://vsthemes.org/en/skins/discord/ and here: https://bdeditor.dev/. Copy the text into the corresponding custom css file. */")
            
        time.sleep(2) # Wait to be sure of the file creation
        
        stdscr.addstr(6, 0, f"Opening '{filename}'...")
        openDefaultEditor(css_file_path)
        
        rawInput(stdscr, 7, 0, "Press enter to save your custom CSS.")
        stdscr.addstr(8, 0, f"You can still modify it by going here {css_file_path}.")
        rawInput(stdscr, 9, 0, "Press enter to finish.")
        state = STATE_MAIN_MENU
        
    stdscr.refresh()
        
def displaySelectCustomCSS(stdscr, current_selection, customcss_data):
    global state
    
    with open('JSON/config.json', 'r') as json_file:
        config_data = json.load(json_file)

    if(config_data["custom-css-initiated"] == False):
        rawInput(stdscr, 0, 0, "PRESS ENTER TO INITIATE CUSTOM CSS")
        initCustomCSS()
        
    stdscr.addstr(0, 0, "                                ")
    
    customs_css = list(customcss_data.keys())
    revert = "Revert"
    customs_css.append(revert)
    
    for i, custom_css in enumerate(customs_css):
        if i == current_selection:
            stdscr.addstr(i + 3, 0, f"> {custom_css}", curses.color_pair(1) | curses.A_BOLD)
        else:
            stdscr.addstr(i + 3, 0, f"  {custom_css}")
            
    stdscr.refresh()
            
def displayDeleteCustomCSS(stdscr, current_selection, customcss_data, deleteCSSVerification):
    global state
    
    stdscr.addstr(0, 0, "Delete Custom CSS: \nPress enter twice to delete the selected one.")
    
    customs_css = list(customcss_data.keys())
    customs_css.pop(0)
    
    for i, custom_css in enumerate(customs_css):
        if i == current_selection:
            stdscr.addstr(i + 3, 0, f"> {custom_css}", curses.color_pair(1) | curses.A_BOLD)
        else:
            stdscr.addstr(i + 3, 0, f"  {custom_css}")
            
    if(deleteCSSVerification == True):
        stdscr.addstr(current_selection + 3, len(list(customcss_data.keys())[current_selection]) + 5, "Press again to delete.", curses.color_pair(3))
    
    stdscr.refresh()


def githubPage():
    webbrowser.open('https://github.com/Locox-dev/FlowCord')
    
def discordLink():
    webbrowser.open('https://discord.gg/7jU3nWjqGX')

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
    subprocess.run(node_cmd, shell=True)
    
def setCustomCSS(selected, selected_css):
    global customCSS
    global customCSSName
    py_cmd = ["python", "customcss.py", "--file", selected_css]
    subprocess.run(py_cmd, shell=True)
    config_data = None
    with open('JSON/config.json', 'r') as json_file:
        config_data = json.load(json_file)
    config_data["custom-css-used"] = selected
    with open('JSON/config.json', 'w') as json_file:
        json.dump(config_data, json_file, indent=4)
    customCSS = True
    customCSSName = selected

def setDefaultCSS():
    global customCSS
    global customCSSName
    py_cmd = ["python", "customcss.py", "--default"]
    subprocess.run(py_cmd, shell=True)
    config_data = None
    with open('JSON/config.json', 'r') as json_file:
        config_data = json.load(json_file)
    config_data["custom-css-used"] = ""
    with open('JSON/config.json', 'w') as json_file:
        json.dump(config_data, json_file, indent=4)
    customCSS = False
    customCSSName = ""

def initCustomCSS():
    py_cmd = ["python", "customcss.py"]
    subprocess.run(py_cmd, shell=True)
    
def revertCustomCSS():
    global customCSS
    global customCSSName
    py_cmd = ["python", "customcss.py", "--revert"]
    subprocess.run(py_cmd, text=True, shell=True)
    customCSS = False
    customCSSName = ""
    
def isItExit(text):
    global state
    if(text == "exit()"):
        state = STATE_MAIN_MENU
        return True
    else:
        return False

def main(stdscr):

    global state
    global richPresence
    global richPresenceName


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
        ["Help", "Github Page", "Discord"],
        ["Create Rich Presence", "Select Rich Presence", "Delete Rich Presence"],
        ["Create Custom CSS", "Select Custom CSS", "Delete Custom CSS"]
    ]
    current_column = 0
    current_row = 0
    current_row_select_rich_presence = 0
    current_row_delete_rich_presence = 0
    current_row_select_custom_css = 0
    current_row_delete_custom_css = 0
    
    deleteVerification = False
    deleteCSSVerification = False
    
    back_button = [
        ["Back (Escape)"]
    ]

    with open('JSON/config.json', 'r') as json_file:
        config_data = json.load(json_file)

    with open("JSON/richpresence.json", "r") as json_file:
        richpresence_data = json.load(json_file)
        
    with open('JSON/customcss.json', 'r') as json_file:
        customcss_data = json.load(json_file)

    while True:
        stdscr.clear()

        if(state == STATE_MAIN_MENU):
            displayMainMenu(stdscr, ascii_title, menu_options, current_column, current_row)
        elif(state == STATE_HELP):
            displayHelp(stdscr, back_button)
        elif(state == STATE_CREATE_RICH_PRESENCE):
            displayCreateRichPresence(stdscr, richpresence_data)
        elif(state == STATE_SELECT_RICH_PRESENCE):
            displaySelectRichPresence(stdscr, richpresence_data, current_row_select_rich_presence)
        elif(state == STATE_DELETE_RICH_PRESENCE):
            displayDeleteRichPresence(stdscr, richpresence_data, current_row_delete_rich_presence, deleteVerification)
        elif(state == STATE_CREATE_CUSTOM_CSS):
            displayCreateCustomCSS(stdscr, customcss_data)
        elif(state == STATE_SELECT_CUSTOM_CSS):
            displaySelectCustomCSS(stdscr, current_row_select_custom_css, customcss_data)
        elif(state == STATE_DELETE_CUSTOM_CSS):
            displayDeleteCustomCSS(stdscr, current_row_delete_custom_css, customcss_data, deleteCSSVerification)

        if(config_data["custom-css-used"] != "" or customCSS == True):
            if(customCSS == True):
                stdscr.addstr(terminal_height - 2, 0, "Custom CSS '" + customCSSName + "' currently used.", curses.color_pair(2))
            else:
                stdscr.addstr(terminal_height - 2, 0, "Custom CSS '" + config_data["custom-css-used"] + "' currently used.", curses.color_pair(2))
        if(richPresence == True):
            stdscr.addstr(terminal_height - 1, 0, richPresenceName + " running.", curses.color_pair(2))



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
                if(selected_option == "Discord"):
                    discordLink()
                if(selected_option == "Create Rich Presence"):
                    state = STATE_CREATE_RICH_PRESENCE
                if(selected_option == "Select Rich Presence"):
                    state = STATE_SELECT_RICH_PRESENCE
                if(selected_option == "Delete Rich Presence"):
                    state = STATE_DELETE_RICH_PRESENCE
                    deleteVerification = False
                if(selected_option == "Create Custom CSS"):
                    state = STATE_CREATE_CUSTOM_CSS
                if(selected_option == "Select Custom CSS"):
                    state = STATE_SELECT_CUSTOM_CSS
                if(selected_option == "Delete Custom CSS"):
                    state = STATE_DELETE_CUSTOM_CSS
        elif(state == STATE_SELECT_RICH_PRESENCE):
            if (key == ord('z') or key == curses.KEY_UP):
                current_row_select_rich_presence = max(current_row_select_rich_presence - 1, 0)
            elif (key == ord('s') or key == curses.KEY_DOWN):
                current_row_select_rich_presence = min(current_row_select_rich_presence + 1, len(list(richpresence_data.keys())) - 1)
            elif (key == ord('\n') or key == ord(' ')):
                selected = list(richpresence_data.keys())[current_row_select_rich_presence]

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
                current_row_delete_rich_presence = min(current_row_delete_rich_presence + 1, len(list(richpresence_data.keys())) - 1)
                deleteVerification = False
            elif (key == ord('\n') or key == ord(' ')):
                selected = list(richpresence_data.keys())[current_row_delete_rich_presence]
                if(deleteVerification == False):
                    deleteVerification = True
                else:
                    if(selected in richpresence_data):
                        del richpresence_data[selected]

                    with open('JSON/richpresence.json', 'w') as json_file:
                        json.dump(richpresence_data, json_file, indent=4)
                        
                    deleteVerification = False
        elif(state == STATE_SELECT_CUSTOM_CSS):
            if (key == ord('z') or key == curses.KEY_UP):
                current_row_select_custom_css = max(current_row_select_custom_css - 1, 0)
            elif (key == ord('s') or key == curses.KEY_DOWN):
                current_row_select_custom_css = min(current_row_select_custom_css + 1, len(list(customcss_data.keys())))
            elif (key == ord('\n') or key == ord(' ')):
                customs_css = list(customcss_data.keys())
                revert = "Revert"
                customs_css.append(revert)
                selected = list(customs_css)[current_row_select_custom_css]
            
                if(selected == "Revert"):
                    revertCustomCSS()
                else:
                    selected_css = customcss_data[selected]
                
                    if(selected_css == "DISABLE"):
                        setDefaultCSS()
                    else:
                        setCustomCSS(selected, selected_css)
                state = STATE_MAIN_MENU
        elif(state == STATE_DELETE_CUSTOM_CSS):
            if (key == ord('z') or key == curses.KEY_UP):
                current_row_delete_custom_css = max(current_row_delete_custom_css - 1, 0)
            elif (key == ord('s') or key == curses.KEY_DOWN):
                current_row_delete_custom_css = min(current_row_delete_custom_css + 1, len(list(customcss_data.keys())) - 1)
            elif (key == ord('\n') or key == ord(' ')):
                revert = "Revert"
                customs_css.append(revert)
                selected = list(customcss_data.keys())[current_row_delete_custom_css + 1]
                selected_css = customcss_data[selected]
                if(deleteCSSVerification == False):
                    deleteCSSVerification = True
                else:
                    if(selected in customcss_data):
                        del customcss_data[selected]

                    with open('JSON/customcss.json', 'w') as json_file:
                        json.dump(customcss_data, json_file, indent=4)
                        
                    os.remove(selected_css)
                        
                    deleteCSSVerification = False
        elif(state == STATE_HELP):
            if (key == ord('\n') or key == ord(' ')):
                state = STATE_MAIN_MENU

        if key == 27:
            if(state == STATE_MAIN_MENU):
                exit()
            state = STATE_MAIN_MENU

        stdscr.refresh()

if __name__ == "__main__":
    if(platform.release() == "10"):
        system(f'mode con: cols={terminal_width} lines={terminal_height}') # Resize terminal window ONLY ON WINDOWS 10
    else:
        print("To make sure the program work properly, please set the terminal size to fullscreen using F11 or the square button.")
        print("Time before starting:")
        print("10")
        time.sleep(1)
        print("9")
        time.sleep(1)
        print("8")
        time.sleep(1)
        print("7")
        time.sleep(1)
        print("6")
        time.sleep(1)
        print("5")
        time.sleep(1)
        print("4")
        time.sleep(1)
        print("3")
        time.sleep(1)
        print("2")
        time.sleep(1)
        print("1")
        time.sleep(1)
        print("Starting...")
        time.sleep(1)
    curses.wrapper(main)
