from pathlib import Path
import os
import json
import config_utils
import questionary


def main():
    config_file = Path(config_utils.CONFIG_PATH)

    if not config_file.exists():
        config_utils.create_config_file()

    with open(config_utils.CONFIG_PATH, "r") as file:
        data = json.load(file)

    display_start_screen()


if __name__ == "__main__":
    main()


def display_start_screen():
    option = questionary.select(
        "Select option:", choices=["Track profiles", "Car profiles", "Settings"]
    ).ask()

    print(option)
