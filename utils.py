import json
import os

import questionary


def get_paths_list(path, item_list):
    path_list = []

    for item in item_list:
        path_list.append(f"{path}\\{item}")

    return path_list


def filter_remove(items, sources):
    filtered_items = []
    for item in items:
        if item in sources:
            filtered_items.append(item)

    return filtered_items


def write_to_json(path, data):
    with open(path, "w") as file:
        json.dump(data, file, indent=2)


def get_data(path):
    with open(path, "r") as file:
        data = json.load(file)

    return data


def get_folder_path(folder):
    folder_path = ""

    while True:
        folder_path = questionary.path(
            f"Enter the path to your {folder} folder:\n",
            only_directories=True,
            qmark="",
        ).ask()

        confirm = questionary.confirm("Confirm path?").ask()

        if confirm:
            break

    return folder_path


def get_dirs_from_path(path):
    directories = []
    all_files = os.listdir(path)

    for file in all_files:
        if os.path.isdir(f"{path}\\{file}"):
            directories.append(file)

    return directories
