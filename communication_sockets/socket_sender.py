import socket


def send_message(host, port, message):  # possible extension - ConnectionRefusedError
    if not isinstance(message, bytes):
        message = message.encode()
    connection = socket.socket()
    connection.connect((host, port))
    connection.send(message)
    response = connection.recv(256)
    if response == b'ok':
        connection.close()
        return True
    return False


if __name__ == '__main__':
    import time
    hostq = 'localhost'
    portq = 55555
    while True:
        send_message(hostq, portq, b'ping msg')
        time.sleep(1)
