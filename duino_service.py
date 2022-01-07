import time
from threading import Thread
from serial_control.serial_class import DuinoSerial
from serial_control.read_script import check_duino_json, update_duino_json
from settings import port, json_temp_file_path, logfile_path, save_result_timeout


command = None
result_dict = {}


def communicate_with_serial(duino_serial):
    global command
    global result_dict

    while True:
        if command:
            duino_serial.send_command(command)
            command = None

        json_line = duino_serial.read_line_json()
        if json_line:
            result_dict.update(json_line)
        time.sleep(0.3)


def main():
    global command
    global result_dict
    duino_serial = DuinoSerial(port)

    command = None
    read_timer = time.monotonic()

    communicate_thread = Thread(target=communicate_with_serial, args=(duino_serial,))
    communicate_thread.start()

    while True:

        if read_timer < time.monotonic():  # save dict to json
            result_dict = check_duino_json(result_dict)
            update_duino_json(result_dict, json_temp_file_path, logfile_path)
            result_dict = {}

            read_timer = time.monotonic() + save_result_timeout


if __name__ == "__main__":
    main()
