import sys

from communication_sockets.socket_sender import send_message
from settings import socket_port, socket_host


commands = {
    "light_on": b"light on",
    "light_off": b"light off",
    "relay_on": b"relay on",
    "relay_off": b"relay off",
}

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.stdout.write("Need command, available commands: {}".format(commands.keys()))
        sys.exit(1)

    command = sys.argv[1]

    cmd_to_send = commands.get(command)
    if cmd_to_send:
        send_message(socket_host, socket_port, cmd_to_send)
    else:
        sys.stdout.write("Write available command")
