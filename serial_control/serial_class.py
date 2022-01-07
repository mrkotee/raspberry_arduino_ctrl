
import time
import json
import serial


class DuinoSerial:

    def __init__(self, port):
        try:
            self.connect = serial.Serial(port, 9600, timeout=0.3)
        except FileNotFoundError:
            print('port not found')
        self.connect.reset_input_buffer()

    def read(self):
        if self.connect.in_waiting > 0:
            line = self.connect.readline().decode('utf-8').rstrip()
            return line
        else:
            return None

    def read_line_json(self):
        line = self.read()
        if line:
            try:
                data = json.loads(line)
                return data
            except json.decoder.JSONDecodeError:
                print(line)
        return None

    def read_full_json(self, wait_time=60, duino_dict_len=1):
        """

        :param wait_time: time for waiting full dict
        :param duino_dict_len: len of dict is waiting for
        :return: dict
        example return: {
            {"temp in": 24.47}
            {"humidity": 13.00}
            {"temp dht": 26.40}
            {"temp out": 24.64}
            }
        """
        result_dict = {}
        timer_prev = time.time()
        timer = 0
        while timer < wait_time and len(result_dict) < duino_dict_len:
            time.sleep(0.1)

            data = self.read_line_json()
            if data:
                result_dict.update(data)

            timer = time.time() - timer_prev
        return result_dict

    def send_command(self, command):
        """

        :param command: command to connected arduino
        :return:
        """

        if not isinstance(command, bytes):
            command = command.encode()
        while self.read() != 'send':
            self.connect.write(command)
            time.sleep(1)

    def _switch(self, cmd, opt):
        if opt:
            cmd += b' on'
        else:
            cmd += b' off'
        self.send_command(cmd)

    def switch_light(self, option=True):
        self._switch(b'light', option)

    def switch_relay(self, option=True):
        self._switch(b'relay', option)

