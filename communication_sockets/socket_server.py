import asyncio
import socket
import time

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
            conn.close()
        time.sleep(0.3)


async def handle_client(client):
    global socket_data
    loop = asyncio.get_event_loop()

    while True:
        socket_data = await loop.sock_recv(client, 256)
        await loop.sock_sendall(client, b"ok")


async def socket_listen(host, port):
    sock = socket.socket()

    sock.bind((host, port))
    sock.listen(1)

    loop = asyncio.get_event_loop()

    while True:
        client, _ = await loop.sock_accept(sock)
        loop.create_task(handle_client(client))
        print('asdf')


if __name__ == "__main__":
    hostq = 'localhost'
    portq = 55555
    # asyncio.run(socket_listen(hostq, portq))

    from threading import Thread

    thr = Thread(target=threaded_server, args=(hostq, portq), daemon=True)
    thr.start()

    while True:
        if socket_data:
            print(f'{socket_data=}')
            socket_data = ""
        time.sleep(0.5)
