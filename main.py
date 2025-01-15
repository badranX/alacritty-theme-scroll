import curses

def main(stdscr):
    # Disable cursor
    curses.curs_set(0)

    # Sample list of items
    items = [f"Item {i+1}" for i in range(20)]

    # Index of the currently selected item
    current_index = 0
    search_query = ""

    # Main loop
    while True:
        stdscr.clear()

        # Display the instruction message
        stdscr.addstr(0, 0, "Please, select your item: \n")

        # Display the search bar
        stdscr.addstr(1, 0, f"Search: {search_query}\n")

        # Calculate the range of items to display
        start_index = max(0, current_index - 3)
        end_index = min(len(items), current_index + 4)

        # Display items with highlighting for the current selection
        for idx in range(start_index, end_index):
            if idx == current_index:
                stdscr.addstr(idx - start_index + 2, 0, items[idx], curses.A_REVERSE)
            else:
                stdscr.addstr(idx - start_index + 2, 0, items[idx])

        # Refresh the screen
        stdscr.refresh()

        # Get user input
        key = stdscr.getch()

        # Handle user input
        if key == curses.KEY_UP:
            current_index = max(0, current_index - 1)
        elif key == curses.KEY_DOWN:
            current_index = min(len(items) - 1, current_index + 1)
        elif key == ord('q'):
            break
        elif key == ord('\n'):
            stdscr.clear()
            stdscr.addstr(0, 0, f"You selected: {items[current_index]}\n")
            stdscr.refresh()
            stdscr.getch()
            break
        elif key == 27:  # Escape key to clear search
            search_query = ""
        elif key in range(32, 127):  # Add printable characters to search query
            search_query += chr(key)
            # Jump to the first matching item
            matching_indices = [i for i, item in enumerate(items) if search_query.lower() in item.lower()]
            if matching_indices:
                current_index = matching_indices[0]
        elif key == curses.KEY_BACKSPACE or key == 127:  # Handle backspace
            search_query = search_query[:-1]
            # Jump to the first matching item if the query is not empty
            if search_query:
                matching_indices = [i for i, item in enumerate(items) if search_query.lower() in item.lower()]
                if matching_indices:
                    current_index = matching_indices[0]

if __name__ == "__main__":
    curses.wrapper(main)


