from pathlib import Path
import os
import utils

SYMLINK_PATH = "symlinks.json"


def update_car_symlinks(data):
    symlink_file = Path(SYMLINK_PATH)

    if not symlink_file.exists():
        create_symlink_file()
        symlink_file = Path(SYMLINK_PATH)

    symlinks = utils.get_data(symlink_file)

    car_paths_to_add = []
    car_paths_to_remove = []

    for profile in data["car_profiles"]:
        path = f"{data['cars_path']}\\{profile['profile']}"
        if profile["status"]:
            car_paths_to_add.append(utils.get_paths_list(path, profile["items"]))
        else:
            car_paths_to_remove.append(utils.get_paths_list(path, profile["items"]))

    car_paths_to_add = sum(car_paths_to_add, [])
    add_car_symlinks(
        car_paths_to_add, symlinks, f"{data['assetto_path']}\\content\\cars"
    )

    car_paths_to_remove = sum(car_paths_to_remove, [])
    remove_car_symlinks(car_paths_to_remove, symlinks)


def add_car_symlinks(car_paths, symlinks, dest_path):
    cars_src = []
    for car in symlinks["cars"]:
        cars_src.append(car["src"])

    car_paths_to_add = list(set(car_paths) - set(cars_src))

    for car in car_paths_to_add:
        car_link = create_symlink(car, dest_path)
        symlinks["cars"].append(car_link)

    utils.write_to_json(SYMLINK_PATH, symlinks)


def remove_car_symlinks(car_paths, symlinks):
    cars_src = []
    for car in symlinks["cars"]:
        cars_src.append(car["src"])

    car_paths_to_remove = utils.filter_remove(car_paths, cars_src)

    for car_path in car_paths_to_remove:
        car = next(car for car in symlinks["cars"] if car["src"] == car_path)
        remove_symlink(car["dest"])
        symlinks["cars"].remove(car)

    utils.write_to_json(SYMLINK_PATH, symlinks)


def update_track_symlinks(data):
    symlink_file = Path(SYMLINK_PATH)

    if not symlink_file.exists():
        create_symlink_file()
        symlink_file = Path(SYMLINK_PATH)

    symlinks = utils.get_data(SYMLINK_PATH)

    track_paths_to_add = []
    track_paths_to_remove = []

    for profile in data["track_profiles"]:
        path = f"{data['tracks_path']}\\{profile['profile']}"
        if profile["status"]:
            track_paths_to_add.append(utils.get_paths_list(path, profile["items"]))
        else:
            track_paths_to_remove.append(utils.get_paths_list(path, profile["items"]))

    track_paths_to_add = sum(track_paths_to_add, [])
    add_track_symlinks(
        track_paths_to_add, symlinks, f"{data['assetto_path']}\\content\\tracks"
    )

    track_paths_to_remove = sum(track_paths_to_remove, [])
    remove_track_symlinks(track_paths_to_remove, symlinks)


def add_track_symlinks(track_paths, symlinks, dest_path):
    tracks_src = []
    for track in symlinks["tracks"]:
        tracks_src.append(track["src"])

    track_paths_to_add = list(set(track_paths) - set(tracks_src))

    for track in track_paths_to_add:
        track_link = create_symlink(track, dest_path)
        symlinks["tracks"].append(track_link)

    utils.write_to_json(SYMLINK_PATH, symlinks)


def remove_track_symlinks(track_paths, symlinks):
    tracks_src = []
    for track in symlinks["tracks"]:
        tracks_src.append(track["src"])

    track_paths_to_remove = utils.filter_remove(track_paths, tracks_src)

    for track_path in track_paths_to_remove:
        track = next(
            track for track in symlinks["tracks"] if track["src"] == track_path
        )
        remove_symlink(track["dest"])
        symlinks["tracks"].remove(track)

    utils.write_to_json(SYMLINK_PATH, symlinks)


def create_symlink_file():
    data = {"tracks": [], "cars": []}

    utils.write_to_json(SYMLINK_PATH, data)


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


def remove_all_symlinks(symlinks):
    for car in symlinks["cars"]:
        remove_symlink(car["dest"])

    for track in symlinks["tracks"]:
        remove_symlink(track["dest"])

    create_symlink_file()

    print("All symlinks removed")
