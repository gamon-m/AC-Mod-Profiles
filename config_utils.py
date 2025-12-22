from questionary import Choice
from symlink_utils import update_car_symlinks, update_track_symlinks
import utils

CONFIG_PATH = "config.json"


def get_assetto_path():
    return utils.get_folder_path("Assetto Corsa")


def get_tracks_path():
    return utils.get_folder_path("track mods")


def get_cars_path():
    return utils.get_folder_path("car mods")


def make_profiles(path):
    profile_list = utils.get_dirs_from_path(path)

    profiles = []

    for profile in profile_list:
        items = get_items(f"{path}\\{profile}")
        profiles.append({"profile": profile, "status": False, "items": items})

    return profiles


def get_items(path):
    item_list = utils.get_dirs_from_path(path)

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

    utils.write_to_json(CONFIG_PATH, data)


def toggle_profiles(profiles, selected):
    for profile in profiles:
        if profile["profile"] in selected:
            profile["status"] = True
        else:
            profile["status"] = False

    return profiles


def get_choices(profiles):
    choices = []

    for profile in profiles:
        choices.append(Choice(profile["profile"], checked=profile["status"]))

    return choices


def save_track_profiles(data, profiles):
    data["track_profiles"] = profiles

    utils.write_to_json(CONFIG_PATH, data)
    update_track_symlinks(data)

    print("Saved track profiles.")


def save_car_profiles(data, profiles):
    data["car_profiles"] = profiles

    utils.write_to_json(CONFIG_PATH, data)
    update_car_symlinks(data)

    print("Saved car profiles.")
