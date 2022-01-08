import os
import time
import socket
from threading import Thread
import logging
from serial_control.serial_class import DuinoSerial
from serial_control.read_script import check_duino_json, update_duino_json
# from communication_sockets.socket_server import threaded_server
from settings import port, json_temp_file_path, logfile_path, logging_level, save_result_timeout, socket_port, socket_host

logging.basicConfig(filename=logfile_path, level=logging_level,
                    format='%(asctime)s -  %(levelname)s: %(message)s')

command = None
result_dict = {}
socket_data = b""


def threaded_server(host, port):
    global socket_data

    sock = socket.socket()

    sock.bind((host, port))
    sock.listen(1)

    while True:
        conn, addr = sock.accept()
        if conn:
            data = conn.recv(1024)
            if data:
                socket_data = data
                conn.send(b'ok')
                logging.info(f'receive command: {socket_data}')
            conn.close()
        time.sleep(0.3)


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
            logging.debug(f'{json_line}')
        time.sleep(0.3)


def main():
    global command
    global result_dict
    global socket_data
    duino_serial = DuinoSerial(port)

    command = None
    read_timer = time.monotonic() + save_result_timeout

    communicate_thread = Thread(target=communicate_with_serial, args=(duino_serial,), daemon=True)
    communicate_thread.start()

    socket_server_thread = Thread(target=threaded_server, args=(socket_host, socket_port), daemon=True)
    socket_server_thread.start()

    while True:

        if read_timer < time.monotonic():  # save dict to json
            result_dict = check_duino_json(result_dict)
            update_duino_json(result_dict, json_temp_file_path)
            logging.info(f'{result_dict}')
            result_dict = {}

            read_timer = time.monotonic() + save_result_timeout

        if socket_data:
            command = socket_data
            socket_data = b""

        time.sleep(0.3)


if __name__ == "__main__":
    main()

