
import sys
import os
import json
import time
from serial_class import DuinoSerial
from settings import port, read_json_timeout, json_temp_file_path, logfile_path


def read_duino_json():
    temp_dict = json.load(open(json_temp_file_path))

    ds = DuinoSerial(port)
    result = ds.read_json(read_json_timeout)

    if len(sys.argv) > 1 and sys.argv[1] == 'log':
        with open(logfile_path, 'a') as f:
            f.write("{}: {}\n".format(time.asctime(time.localtime(time.time())), result))

    if 'relay work' not in result:
        temp_dict['relay work'] = 0

    if 'temp out' not in result:
        temp_dict['temp out'] = None

    temp_dict.update(result)
    json.dump(temp_dict, open(json_temp_file_path, 'w'))
