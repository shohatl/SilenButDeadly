import time
import tqdm
import os
import socket
import rsa
from Crypto.Cipher import AES
import tqdm
from Crypto.Random import get_random_bytes

server_ip = '192.168.68.122'
port = 786


def initiate():
    client_socket = socket.socket()
    client_socket.connect((server_ip, port))
    print('connection initiated')
    n, e = client_socket.recv(1024).decode().split(':')
    n = int(n)
    e = int(e)
    temp_key = rsa.PublicKey(n, e)
    encryption_key = get_random_bytes(32)
    client_socket.send(rsa.encrypt(encryption_key, temp_key))
    return client_socket, encryption_key


def encrypt(data, key):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return cipher.nonce + ciphertext + tag

def decrypt(data, key):
    nonce = data[:16]
    ciphertext = data[16:-16]
    tag = data[-16:]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)


def send(client_socket, encryption_key, filename, path):
    filesize = os.path.getsize(path + filename)
    client_socket.send(encrypt(f'{filename}:{filesize}'.encode(), encryption_key))
    time.sleep(0.1)
    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True,
                         unit_divisor=992)
    with open(path + filename, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(992)
            if not bytes_read:
                # file transmitting is done
                break
            client_socket.sendall(encrypt(bytes_read, encryption_key))
            # update the progress bar
            progress.update(len(bytes_read))


def receive(client_socket, encryption_key, filedata, path):
    filename, filesize = filedata.split(':')
    filesize = int(filesize)

    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True,
                         unit_divisor=992)
    with open(path + filename, "wb") as f:
        while True:
            # read 1024 bytes from the socket (receive)
            bytes_read = client_socket.recv(1024)
            if not bytes_read:
                # nothing is received
                # file transmitting is done
                os.fsync(f.fileno())
                break
            # write to the file the bytes we just received
            bytes_read = decrypt(bytes_read, encryption_key)
            f.write(bytes_read)
            f.flush()
            # update the progress bar
            progress.update(len(bytes_read))
            os.fsync(f.fileno())
        f.close()
    print('down')
