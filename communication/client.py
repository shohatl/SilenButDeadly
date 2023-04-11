import socket
import sys

import rsa
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

if __name__ == '__main__':
    server_ip = '127.0.0.1'
    client_socket = socket.socket()
    client_socket.connect((server_ip, 786))
    print('connection initiated')
    keep_alive = True
    n, e = client_socket.recv(1024).decode().split(':')
    n = int(n)
    e = int(e)
    temp_key = rsa.PublicKey(n, e)
    encryption_key = get_random_bytes(32)
    while (keep_alive):
        cipher = AES.new(encryption_key, AES.MODE_EAX)
        client_socket.send(rsa.encrypt(encryption_key, temp_key))
        data = cipher.encrypt('works'.encode())
        client_socket.send(cipher.nonce + data)

        nonce = cipher.nonce
        cipher = AES.new(encryption_key, AES.MODE_EAX, nonce)
        print(cipher.decrypt(data))
