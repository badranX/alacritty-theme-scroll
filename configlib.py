import toml
from pathlib import Path
import os

from git import Repo


THEMES_FOLDER = 'cli_alacritty_themes'
GIT_REPOS = ['https://github.com/alacritty/alacritty-theme']


class Config():
    def __init__(self):
        self.config_path = self.find_alacritty_config_path()
        with open(self.config_path, 'r') as file:
            self.original = toml.load(file)
            self.config_path = self.find_alacritty_config_path()
            config_dir = os.path.abspath(os.path.dirname(self.config_path))
            self.themes_folder = os.path.join(config_dir, THEMES_FOLDER)

        if not os.path.exists(self.themes_folder):
            os.makedirs(self.themes_folder)
            print('a theme folder was created: ', self.themes_folder)
            for repo in GIT_REPOS:
                Repo.clone_from(repo, self.themes_folder, depth=1, single_branch=True)

    def reset(self):
        with open(self.config_path, 'w') as file:
            toml.dump(self.original, file)

    def find_toml_files(self):
        """
        Recursively finds all .toml files starting from the given directory.

        Returns:
            list of tuples: Each tuple contains the file name (without extension) and the full real path.
        """
        toml_files = []
        realpaths = []

        for root, _, files in os.walk(self.themes_folder):
            for file in files:
                if file.endswith(".toml"):
                    file_name = os.path.splitext(file)[0]
                    full_path = os.path.realpath(os.path.join(root, file))
                    toml_files.append(file_name)
                    realpaths.append(full_path)

        return toml_files, realpaths

    def update_toml_file(self, string_variable):
        try:
            with open(self.config_path, 'r') as file:
                data = toml.load(file)
        except FileNotFoundError:
            data = {}

        if 'import' not in data:
            data['import'] = []

        if not isinstance(data['import'], list):
            raise Exception("The 'import' keyword in the configs is expected to be a list")

        data['import'] = [item for item in data['import'] if str(self.themes_folder) not in item]

        # Add the new value
        data['import'].append(string_variable)

        with open(self.config_path, 'w') as file:
            toml.dump(data, file)


    def find_alacritty_config_path(self):
        """
        Locate the alacritty.toml configuration file.

        Returns:
            str: The path to the first found configuration file, or None if not found.
        """
        config_locations = []

        if os.name == 'nt':  # Windows
            appdata = os.getenv('APPDATA')
            if appdata:
                config_locations.append(os.path.join(appdata, 'alacritty', 'alacritty.toml'))
        else:  # UNIX-based systems
            xdg_config_home = os.getenv('XDG_CONFIG_HOME', os.path.join(Path.home(), '.config'))
            home = str(Path.home())

            config_locations.extend([
                os.path.join(xdg_config_home, 'alacritty', 'alacritty.toml'),
                os.path.join(xdg_config_home, 'alacritty.toml'),
                os.path.join(home, '.config', 'alacritty', 'alacritty.toml'),
                os.path.join(home, '.alacritty.toml')
            ])

        for config_path in config_locations:
            if os.path.isfile(config_path):
                return config_path

        return None


if __name__ == "__main__":
    update_toml_file("test")
