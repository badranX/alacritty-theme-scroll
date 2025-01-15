import toml

CONFIG_FILE = "/home/badranx/.config/alacritty/alacritty.toml"
KEY_WORD = "badranx_alacritty_theme"

def update_toml_file(string_variable, file_path=CONFIG_FILE, keyword=KEY_WORD):
    try:
        with open(file_path, 'r') as file:
            data = toml.load(file)
    except FileNotFoundError:
        data = {}

    if 'import' not in data:
        data['import'] = []

    if not isinstance(data['import'], list):
        raise Exception("The 'import' keyword in the configs is expected to be a list")

    data['import'] = [item for item in data['import'] if keyword not in item]

    # Add the new value
    data['import'].append(string_variable)

    with open(file_path, 'w') as file:
        toml.dump(data, file)


if __name__ == "__main__":
    update_toml_file("test" + KEY_WORD)
