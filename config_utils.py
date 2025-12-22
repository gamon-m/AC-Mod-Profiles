import os
import json
import questionary
from questionary import Choice
from pathlib import Path

CONFIG_PATH = "config.json"
SYMLINK_PATH = "symlinks.json"


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

    write_to_json(SYMLINK_PATH, data)


def add_car_symlinks(car_paths, symlinks, dest_path):
    cars_src = []
    for car in symlinks["cars"]:
        cars_src.append(car["src"])

    car_paths_to_add = list(set(car_paths) - set(cars_src))

    for car in car_paths_to_add:
        link = create_symlink(car, dest_path)
        symlinks["cars"].append(link)

    write_to_json(SYMLINK_PATH, symlinks)


def remove_car_symlinks(car_paths, symlinks):
    cars_src = []
    for car in symlinks["cars"]:
        cars_src.append(car["src"])

    car_paths_to_remove = filter_remove(car_paths, cars_src)

    for car_path in car_paths_to_remove:
        car = next(car for car in symlinks["cars"] if car["src"] == car_path)
        remove_symlink(car["dest"])
        symlinks["cars"].remove(car)

    write_to_json(SYMLINK_PATH, symlinks)


def update_car_symlinks(data):
    symlink_file = Path(SYMLINK_PATH)

    if not symlink_file.exists():
        create_symlink_file()
        symlink_file = Path(SYMLINK_PATH)

    with open(symlink_file, "r") as file:
        symlinks = json.load(file)

    car_paths_to_add = []
    car_paths_to_remove = []

    for profile in data["car_profiles"]:
        path = f"{data['cars_path']}\\{profile['profile']}"
        if profile["status"]:
            car_paths_to_add.append(get_paths_list(path, profile["items"]))
        else:
            car_paths_to_remove.append(get_paths_list(path, profile["items"]))

    car_paths_to_add = sum(car_paths_to_add, [])
    add_car_symlinks(car_paths_to_add, symlinks, data["assetto_path"])

    car_paths_to_remove = sum(car_paths_to_remove, [])
    remove_car_symlinks(car_paths_to_remove, symlinks)


def filter_remove(items, sources):
    filtered_items = []
    for item in items:
        if item in sources:
            filtered_items.append(item)

    return filtered_items


def create_symlink(src, dest):
    folder = os.path.split(src)[1]
    dest = f"{dest}\\{folder}"

    try:
        os.symlink(src, dest)
        print(f"Created symlink: {src} -> {dest}")
    except Exception as e:
        print(e)

    return {"src": src, "dest": dest}


def remove_symlink(dest):
    try:
        os.remove(dest)
        print(f"Removed symlink: {dest}")
    except Exception as e:
        print(e)


def get_paths_list(path, item_list):
    path_list = []

    for item in item_list:
        path_list.append(f"{path}\\{item}")

    return path_list


def update_track_symlinks(data):
    symlink_file = Path(SYMLINK_PATH)

    if not symlink_file.exists():
        create_symlink_file()


def save_track_profiles(data, profiles):
    data["track_profiles"] = profiles

    write_to_json(CONFIG_PATH, data)
    update_track_symlinks(data)

    print("Saved track profiles.")


def save_car_profiles(data, profiles):
    data["car_profiles"] = profiles

    write_to_json(CONFIG_PATH, data)
    update_car_symlinks(data)

    print("Saved car profiles.")
