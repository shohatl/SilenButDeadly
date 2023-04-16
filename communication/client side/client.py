import os
import socket
import time

import rsa
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import tqdm


def encrypt(data, key):
    cipher = AES.new(key, AES.MODE_EAX)
    return cipher.nonce + cipher.encrypt(data)


def decrypt(data, key):
    cipher = AES.new(key, AES.MODE_EAX, nonce=data[0:16])
    return cipher.decrypt(data[16:])


def initiate(server_ip, port):
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


if __name__ == '__main__':
    server_ip = '127.0.0.1'
    keep_alive = True
    is_script = True
    while (keep_alive):
        client_socket, encryption_key = initiate(server_ip, 786)
        print('connected')
        if (os.listdir('./output')):
            filename = os.listdir('./output')[0]
            if (filename == 'default.txt'):
                pass
            else:
                client_socket.send(encrypt('<newoutput>'.encode(), encryption_key))
                time.sleep(0.1)
                filesize = os.path.getsize('./output/' + filename)
                client_socket.send(encrypt(f'{filename}:{filesize}'.encode(), encryption_key))

                progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True,
                                     unit_divisor=1008)
                with open('./output/' + filename, "rb") as f:
                    while True:
                        # read the bytes from the file
                        bytes_read = f.read(1008)
                        if not bytes_read:
                            # file transmitting is done
                            client_socket.close()
                            break
                        client_socket.send(encrypt(bytes_read, encryption_key))
                        # update the progress bar
                        progress.update(len(bytes_read))
                os.remove('./output/' + filename)

        elif (not os.listdir('./script') and is_script):
            print('need new script')
            client_socket.send(encrypt('<newscript>'.encode(), encryption_key))
            data = decrypt(client_socket.recv(1024), encryption_key).decode()
            print(data)
            if data != '<nofile>':
                filename, filesize = data.split(':')
                filesize = int(filesize)

                progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True,
                                     unit_divisor=1008)
                with open('./script/' + filename, "wb") as f:
                    while True:
                        # read 1024 bytes from the socket (receive)
                        bytes_read = client_socket.recv(1024)
                        if not bytes_read:
                            # nothing is received
                            # file transmitting is done
                            client_socket.close()
                            break
                        # write to the file the bytes we just received
                        bytes_read = decrypt(bytes_read, encryption_key)
                        f.write(bytes_read)
                        # update the progress bar
                        progress.update(len(bytes_read))
            else:
                is_script = False
        else:
            client_socket.send(encrypt('update'.encode(), encryption_key))
            keep_alive = False
        client_socket.close()
        print('done')
