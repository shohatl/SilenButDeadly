import time
import tqdm
import os
import socket
import rsa
from Crypto.Cipher import AES
import tqdm


def encrypt(data, key):
    cipher = AES.new(key, AES.MODE_EAX)
    return cipher.nonce + cipher.encrypt(data)


def decrypt(data, key):
    cipher = AES.new(key, AES.MODE_EAX, nonce=data[0:16])
    return cipher.decrypt(data[16:])


def send(client_socket, encryption_key, filename, path):
    filesize = os.path.getsize(path + filename)
    client_socket.send(encrypt(f'{filename}:{filesize}'.encode(), encryption_key))
    time.sleep(0.1)
    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True,
                         unit_divisor=1008)
    with open(path + filename, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(1008)
            if not bytes_read:
                # file transmitting is done
                keep_alive = False
                break
            client_socket.send(encrypt(bytes_read, encryption_key))
            # update the progress bar
            progress.update(len(bytes_read))


def receive(client_socket, encryption_key, path):
    data = decrypt(client_socket.recv(1024), encryption_key).decode()
    print(data)
    filename, filesize = data.split(':')
    filesize = int(filesize)

    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True,
                         unit_divisor=1008)
    with open(path + filename, "wb") as f:
        while True:
            # read 1024 bytes from the socket (receive)
            bytes_read = client_socket.recv(1024)
            if not bytes_read:
                # nothing is received
                # file transmitting is done
                break
            # write to the file the bytes we just received
            bytes_read = decrypt(bytes_read, encryption_key)
            f.write(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))