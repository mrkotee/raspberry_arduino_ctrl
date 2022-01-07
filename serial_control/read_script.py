
import sys
import os
import json
import time


def check_duino_json(duino_dict):
    if 'relay work' not in duino_dict:
        duino_dict['relay work'] = 0

    if 'temp out' not in duino_dict:
        duino_dict['temp out'] = None
    return duino_dict


def update_duino_json(duino_json, json_filepath, logfile_path=None):
    temp_dict = json.load(open(json_filepath))

    if logfile_path:
        with open(logfile_path, 'a') as f:
            f.write("{}: {}\n".format(time.asctime(time.localtime(time.time())), duino_json))

    temp_dict.update(duino_json)
    json.dump(temp_dict, open(json_filepath, 'w'))


def main():
    duino_serial = DuinoSerial(port)
    result_dict = duino_serial.read_full_json(waiting_json_timeout, arduino_dict_len)

    result_dict = check_duino_json(result_dict)

    if len(sys.argv) > 1 and sys.argv[1] == 'log':
        update_duino_json(result_dict, json_temp_file_path, logfile_path)
        sys.exit()
    update_duino_json(result_dict, json_temp_file_path)


if __name__ == "__main__":
    from serial_class import DuinoSerial
    from settings import port, waiting_json_timeout, json_temp_file_path, logfile_path, arduino_dict_len
    main()
