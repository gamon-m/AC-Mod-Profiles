from pathlib import Path
import json
import os
import utils

SYMLINK_PATH = "symlinks.json"


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
            car_paths_to_add.append(utils.get_paths_list(path, profile["items"]))
        else:
            car_paths_to_remove.append(utils.get_paths_list(path, profile["items"]))

    car_paths_to_add = sum(car_paths_to_add, [])
    add_car_symlinks(car_paths_to_add, symlinks, data["assetto_path"])

    car_paths_to_remove = sum(car_paths_to_remove, [])
    remove_car_symlinks(car_paths_to_remove, symlinks)


def add_car_symlinks(car_paths, symlinks, dest_path):
    cars_src = []
    for car in symlinks["cars"]:
        cars_src.append(car["src"])

    car_paths_to_add = list(set(car_paths) - set(cars_src))

    for car in car_paths_to_add:
        link = create_symlink(car, dest_path)
        symlinks["cars"].append(link)

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
