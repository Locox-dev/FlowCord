import curses

def read_ascii_title():
    with open("title.txt", "r", encoding="utf-8") as file:
        return file.read().splitlines()

def main(stdscr):
    # Setup
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)   # Make getch() non-blocking

    # Create some UI elements
    ascii_title = read_ascii_title()
    menu_options = [
        ["Help", "Rich Presence", "Option 3"],
        ["Github page", "Option 5", "Option 6"],
        ["Donate", "Option 8", "Option 9"]
    ]
    current_column = 0
    current_row = 0

    while True:
        stdscr.clear()

        # Display ASCII art title
        title_height = len(ascii_title)
        title_left_margin = 2  # Position from the left margin
        for i, line in enumerate(ascii_title):
            stdscr.addstr(i, title_left_margin, line, curses.A_BOLD)

        # Display menu options
        menu_top = title_height + 2  # Position of the first menu option
        for row, options in enumerate(menu_options):
            for col, option in enumerate(options):
                if col == current_column and row == current_row:
                    stdscr.addstr(menu_top + row, col * 15, f"> {option}", curses.A_REVERSE)
                else:
                    stdscr.addstr(menu_top + row, col * 15, f"  {option}")

        # Get user input
        key = stdscr.getch()

        # Handle ZQSD key presses
        if key == ord('z'):  # Z key for moving up
            current_row = max(current_row - 1, 0)
        elif key == ord('s'):  # S key for moving down
            current_row = min(current_row + 1, len(menu_options) - 1)
        elif key == ord('q'):  # Q key for moving left
            current_column = max(current_column - 1, 0)
        elif key == ord('d'):  # D key for moving right
            current_column = min(current_column + 1, len(menu_options[0]) - 1)
        elif key == ord('\n'):
            # Perform some action based on the selected option
            selected_option = menu_options[current_row][current_column]
            stdscr.addstr(menu_top + len(menu_options), 0, f"Selected: {selected_option}")

        stdscr.refresh()

if __name__ == "__main__":
    curses.wrapper(main)
