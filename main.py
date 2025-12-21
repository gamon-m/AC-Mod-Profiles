from pathlib import Path
import os
import json
import config_utils


def create_json_field(field, value, json_file):
    new_field = {field: value}
    json_file.append(new_field)
    return json_file


def update_json_field(field, value, json_file):
    if field in json_file:
        json_file[field] = value
        return json_file

    return create_json_field(field, value, json_file)


config_file = Path(config_utils.CONFIG_PATH)
if not config_file.exists():
    config_utils.create_config_file()

with open(config_utils.CONFIG_PATH, "r") as file:
    data = json.load(file)
