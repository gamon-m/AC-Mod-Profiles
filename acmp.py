from pathlib import Path
import config_utils as cfg
import display


def main():
    config_file = Path(cfg.CONFIG_PATH)

    if not config_file.exists():
        cfg.create_config_file()

    display.display_start_screen()


if __name__ == "__main__":
    main()
