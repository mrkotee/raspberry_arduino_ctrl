
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

    def read_json(self, wait_time=60):
        """

        :param wait_time:
        :return: dict
        example: {
            {"temp in": 24.47}
            {"humidity": 13.00}
            {"temp dht": 26.40}
            {"temp out": 24.64}
            }
        """
        result_dict = {}
        timer_prev = time.time()
        timer = 0
        while timer < wait_time and len(result_dict) < 5:
            time.sleep(0.1)
            line = self.read()
            if line:
                try:
                    data = json.loads(line)
                    result_dict.update(data)
                except json.decoder.JSONDecodeError:
                    print(line)
            timer = time.time() - timer_prev
        return result_dict

    def send_command(self, command):
        """

        :param command: command to connected arduino
        :return:
        """

        if not isinstance(bytes, command):
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

