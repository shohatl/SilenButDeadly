import socket
import rsa
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import tqdm
import FileTransfer


def encrypt(data, key):
    cipher = AES.new(key, AES.MODE_EAX)
    return cipher.nonce + cipher.encrypt(data)


def decrypt(data, key):
    cipher = AES.new(key, AES.MODE_EAX, nonce=data[0:16])
    return cipher.decrypt(data[16:])


if __name__ == '__main__':
    client_socket = socket.socket()
    client_socket.connect(('127.0.0.1', 786))
    print('connection initiated')
    n, e = client_socket.recv(1024).decode().split(':')
    n = int(n)
    e = int(e)
    temp_key = rsa.PublicKey(n, e)
    encryption_key = get_random_bytes(32)
    client_socket.send(rsa.encrypt(encryption_key, temp_key))
    client_socket.send(encrypt('<newpc>'.encode(), encryption_key))
    FileTransfer.receive(client_socket, encryption_key, 'c:\\')


