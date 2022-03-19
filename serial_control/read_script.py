
import json


def check_duino_json(duino_dict: dict):
    """Check values from remote controllers"""
    if duino_dict:
        if 'relay work' not in duino_dict:
            duino_dict['relay work'] = 0

        if 'temp out' not in duino_dict:
            duino_dict['temp out'] = None
    return duino_dict


def update_duino_json(duino_json: dict, json_filepath: str):
    """Update saved JSON data in file"""
    try:
        temp_dict = json.load(open(json_filepath))
    except FileNotFoundError:
        temp_dict = {}

    temp_dict.update(duino_json)
    json.dump(temp_dict, open(json_filepath, 'w'))
