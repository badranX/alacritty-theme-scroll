import curses

from .configlib import Config


NO_CHANGE = "NONE"


def _ui_logic(stdscr):
    conf = Config()
    db, realpaths = conf.find_toml_files()
    realpaths = {k: v for k, v in zip(db, realpaths)}
    extra = [NO_CHANGE, "default"]
    realpaths[extra[0]] = extra[0]
    realpaths[extra[1]] = extra[1]
    db = extra + db
    items = db

    curses.curs_set(0)

    current_index = 0
    search_query = ""

    conf.update_toml_file(realpaths[db[0]])
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Left/Right arrow to decrease/increase opacity.")
        stdscr.addstr(1, 0, "Please, select your theme: \n")
        stdscr.addstr(2, 0, f"Search: {search_query}\n")
        start_index = max(0, current_index - 3)
        end_index = min(len(items), current_index + 4)

        for idx in range(start_index, end_index):
            if idx == current_index:
                stdscr.addstr(idx - start_index + 3, 0, items[idx], curses.A_REVERSE)
            else:
                stdscr.addstr(idx - start_index + 3, 0, items[idx])

        stdscr.refresh()

        # Get user input
        key = stdscr.getch()

        if key == curses.KEY_UP:
            current_index = max(0, current_index - 1)
            conf.update_toml_file(realpaths[items[current_index]])
        elif key == curses.KEY_DOWN:
            current_index = min(len(items) - 1, current_index + 1)
            conf.update_toml_file(realpaths[items[current_index]])
        elif key == curses.KEY_RIGHT:
            conf.plus_opacity()
        elif key == curses.KEY_LEFT:
            conf.minus_opacity()
        elif key == 23:
            search_query = ""
            current_index = 0
            items = db
            conf.update_toml_file(realpaths[db[0]])
        elif key == ord("\n"):
            chosen_item = items[current_index]
            if chosen_item != NO_CHANGE:
                conf.update_toml_file(realpaths[chosen_item])
            stdscr.clear()
            stdscr.addstr(0, 0, f"You selected: {chosen_item}\n")
            stdscr.refresh()
            stdscr.getch()
            return
        elif key == 27:  # Escape key to clear search
            break
        elif key in range(32, 127):  # Add printable characters to search query
            search_query += chr(key)
            matching_indices = [
                item for item in db if search_query.lower() in item.lower()
            ]
            if matching_indices:
                conf.update_toml_file(realpaths[matching_indices[0]])
                current_index = 0
                items = matching_indices
        elif key == curses.KEY_BACKSPACE or key == 127:  # Handle backspace
            search_query = search_query[:-1]
            if search_query:
                matching_indices = [
                    item for item in db if search_query.lower() in item.lower()
                ]
                if matching_indices:
                    conf.update_toml_file(realpaths[matching_indices[0]])
                    current_index = 0
                    items = matching_indices
            else:
                current_index = 0
                items = db
                conf.update_toml_file(realpaths[db[0]])
    # End Loop
    conf.reset()


def run():
    curses.wrapper(_ui_logic)
