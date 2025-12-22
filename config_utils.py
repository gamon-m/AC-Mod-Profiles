import os
import json
import questionary
from questionary import Choice
from pathlib import Path

CONFIG_PATH = "config.json"


def write_to_json(path, data):
    with open(path, "w") as file:
        json.dump(data, file, indent=2)


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


def get_assetto_path():
    return get_folder_path("Assetto Corsa")


def get_tracks_path():
    return get_folder_path("track mods")


def get_cars_path():
    return get_folder_path("car mods")


def get_dirs_from_path(path):
    directories = []
    all_files = os.listdir(path)

    for file in all_files:
        if os.path.isdir(f"{path}\\{file}"):
            directories.append(file)

    return directories


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

    write_to_json(CONFIG_PATH, data)


def toggle_profiles(profiles, selected):
    for profile in profiles:
        if profile["profile"] in selected:
            profile["status"] = True
        else:
            profile["status"] = False

    return profiles


def create_json_field(field, value, json_file):
    new_field = {field: value}
    json_file.append(new_field)
    return json_file


def update_json_field(field, value, json_file):
    if field in json_file:
        json_file[field] = value
        return json_file

    return create_json_field(field, value, json_file)


def get_choices(profiles):
    choices = []

    for profile in profiles:
        choices.append(Choice(profile["profile"], checked=profile["status"]))

    return choices


def get_data():
    with open(CONFIG_PATH, "r") as file:
        data = json.load(file)

    return data


def create_symlink_file():
    data = {"tracks": [], "cars": []}

    write_to_json("symlinks.json", data)


def update_car_symlinks():
    symlink_file = Path("symlinks.json")

    if not symlink_file.exists():
        create_symlink_file()


def update_track_symlinks():
    symlink_file = Path("symlinks.json")

    if not symlink_file.exists():
        create_symlink_file()


def save_track_profiles(data, profiles):
    data["track_profiles"] = profiles

    write_to_json(data)
    update_track_symlinks(data["track_profiles"])

    print("Saved track profiles.")


def save_car_profiles(data, profiles):
    data["car_profiles"] = profiles

    write_to_json(data)
    update_car_symlinks(data["car_profiles"])

    print("Saved car profiles.")
