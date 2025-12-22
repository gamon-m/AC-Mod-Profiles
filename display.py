import questionary
import config_utils as cfg


def display_track_profiles():
    data = cfg.get_data()
    track_profiles = data["track_profiles"]

    option = ""

    while True:
        choices = cfg.get_choices(track_profiles)

        selected_profiles = questionary.checkbox(
            "Select track profiles to enable: ",
            choices=choices,
            instruction="<space> to select, <enter> to confirm, <a> to select all, <i> to invert selection",
            qmark="",
        ).ask()

        questionary.print(f"Selected profiles: {selected_profiles}")

        track_profiles = cfg.toggle_profiles(track_profiles, selected_profiles)

        option = questionary.select(
            "", choices=["Cancel", "Edit selection", "Save and exit"]
        ).ask()

        if not option == "Edit selection":
            break

    if option == "Save and exit":
        cfg.save_track_profiles(data, track_profiles)
    display_start_screen()


def display_car_profiles():
    data = cfg.get_data()
    car_profiles = data["car_profiles"]

    option = ""

    while True:
        choices = cfg.get_choices(car_profiles)

        selected_profiles = questionary.checkbox(
            "Select car profiles to enable",
            choices=choices,
            instruction="<space> to select, <enter> to confirm, <a> to select all, <i> to invert selection",
            qmark="",
        ).ask()

        questionary.print(f"Selected profiles: {selected_profiles}")

        car_profiles = cfg.toggle_profiles(car_profiles, selected_profiles)

        option = questionary.select(
            "", choices=["Cancel", "Edit selection", "Save and exit"]
        ).ask()

        if not option == "Edit selection":
            break

    if option == "Save and exit":
        cfg.save_car_profiles(data, car_profiles)
    display_start_screen()


def display_settings():
    data = cfg.get_data()

    while True:
        option = questionary.select(
            "Select option:",
            choices=[
                "Change Assetto Corsa path",
                "Change track profiles path",
                "Change car profiles path",
                "Reset config",
                "Remove all symlinks",
                "Exit",
            ],
            qmark="",
        ).ask()

        if option == "Exit":
            break

        match option:
            case "Change Assetto Corsa path":
                path = cfg.get_assetto_path()
                data["assetto_path"] = path

                cfg.write_to_json(cfg.CONFIG_PATH, data)
            case "Change track profiles path":
                path = cfg.get_tracks_path()
                track_profiles = cfg.make_profiles(path)

                data["tracks_path"] = path
                data["track_profiles"] = track_profiles

                cfg.write_to_json(cfg.CONFIG_PATH, data)
            case "Change car profiles path":
                path = cfg.get_cars_path()
                car_profiles = cfg.make_profiles(path)

                data["cars_path"] = path
                data["car_profiles"] = car_profiles

                cfg.write_to_json(cfg.CONFIG_PATH, data)
            case "Reset config":
                track_profiles = cfg.make_profiles(data["tracks_path"])
                car_profiles = cfg.make_profiles(data["cars_path"])

                data["track_profiles"] = track_profiles
                data["car_profiles"] = car_profiles

                cfg.write_to_json(cfg.CONFIG_PATH, data)
            case "Remove all symlinks":
                pass

    display_start_screen()


def display_start_screen():
    option = questionary.select(
        "Select option:",
        choices=["Track profiles", "Car profiles", "Settings", "Exit"],
        qmark="",
    ).ask()

    match option:
        case "Track profiles":
            display_track_profiles()
        case "Car profiles":
            display_car_profiles()
        case "Settings":
            display_settings()
        case "Exit":
            pass
