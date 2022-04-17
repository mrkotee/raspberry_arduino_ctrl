import asyncio
import time
import logging
from serial_control.serial_class import DuinoSerial
from serial_control.read_script import check_duino_json, update_duino_json
from settings import port, json_temp_file_path, logfile_path, logging_level, save_result_timeout, socket_port, socket_host

logging.basicConfig(filename=logfile_path, level=logging_level,
                    format='%(asctime)s -  %(levelname)s: %(message)s')


class DuinoService:
    def __init__(self, serial_port, socket_host, socket_port):
        self.command = None
        self.result_dict = {}
        self.socket_data = b""
        self.socket_host = socket_host
        self.socket_port = socket_port
        self.duino_serial = DuinoSerial(serial_port)

    async def get_socket_messages(self, reader, writer):
        while True:
            socket_data = await reader.read(128)
            if not socket_data:
                break
            self.socket_data = socket_data
            writer.write(b"ok")
            await writer.drain()
            logging.info(f'receive command: {self.socket_data}')
            await asyncio.sleep(0.3)
        writer.close()

    async def serial_communicate(self):
        while True:
            if self.command:
                self.duino_serial.send_command(self.command)
                self.command = None
            json_line = self.duino_serial.read_line_json()
            if json_line:
                self.result_dict.update(json_line)
                logging.debug(f'{json_line}')
            await asyncio.sleep(0.3)

    async def handler(self):
        logging.debug("start handler")
        serial_read_timer = time.monotonic() + save_result_timeout
        asyncio.create_task(self.serial_communicate())
        logging.debug("start serial")
        await asyncio.start_server(self.get_socket_messages, self.socket_host, self.socket_port)
        logging.debug("start server")
        while True:
            if serial_read_timer < time.monotonic():  # save dict to json
                self.result_dict = check_duino_json(self.result_dict)
                update_duino_json(self.result_dict, json_temp_file_path)
                logging.info(f'{self.result_dict}')
                self.result_dict = {}
                serial_read_timer = time.monotonic() + save_result_timeout

            if self.socket_data:
                self.command = self.socket_data
                self.socket_data = b""
            await asyncio.sleep(0.3)


if __name__ == "__main__":
    service = DuinoService(port, socket_host, socket_port)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(service.handler())
