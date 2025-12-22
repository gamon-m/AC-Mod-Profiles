import os
from pathlib import Path
import json
import questionary

CONFIG_PATH = "config.json"


def get_folder_path(folder):
    folder_path = ""

    while True:
        folder_path = questionary.path(
            f"Enter the path to your {folder} folder:\n",
            only_directories=True,
            qmark=False,
        ).ask()

        confirm = questionary.confirm("Confirm path?").ask()

        if confirm:
            break

    return folder_path


def get_assetto_path():
    return get_folder_path("Assetto Corsa")


def get_tracks_path():
    return get_folder_path("track mods")


def get_cars_path():
    return get_folder_path("car mods")


def get_dirs_from_path(path):
    return os.listdir(path)


def make_profiles(path):
    profile_list = get_dirs_from_path(path)

    profiles = []

    for profile in profile_list:
        items = get_items(f"{path}\\{profile}")
        profiles.append({"profile": profile, "status": False, "items": items})

    return profiles


def get_items(path):
    item_list = get_dirs_from_path(path)

    items = []

    for item in item_list:
        items.append(item)

    return items


def create_config_file():
    assetto_path = get_assetto_path()
    tracks_path = get_tracks_path()
    cars_path = get_cars_path()

    data = {
        "assetto_path": assetto_path,
        "tracks_path": tracks_path,
        "cars_path": cars_path,
        "track_profiles": [],
        "car_profiles": [],
    }

    track_profiles = make_profiles(tracks_path)
    car_profiles = make_profiles(cars_path)

    data["track_profiles"] = track_profiles
    data["car_profiles"] = car_profiles

    with open(CONFIG_PATH, "w") as file:
        json.dump(data, file, indent=2)


def create_json_field(field, value, json_file):
    new_field = {field: value}
    json_file.append(new_field)
    return json_file


def update_json_field(field, value, json_file):
    if field in json_file:
        json_file[field] = value
        return json_file

    return create_json_field(field, value, json_file)
