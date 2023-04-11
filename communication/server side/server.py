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


if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 786))
    server_socket.listen()
    while (True):
        print('connection initiated')
        client_socket, client_ip = server_socket.accept()
        (public_key, private_key) = rsa.newkeys(1024)
        client_socket.send((str(public_key.n) + ':' + str(public_key.e)).encode())
        encryption_key = rsa.decrypt(client_socket.recv(1024), private_key)

        keep_alive = True
        while (keep_alive):
            scripts = os.listdir('./queue')
            filename = ''
            while (filename == '' and scripts):
                print(scripts)
                if scripts[0].endswith('.py'):
                    filename = scripts[0]
                else:
                    os.remove('./queue/' + scripts[0])
                    scripts = scripts[1:]
            print(filename)
            if filename != '':
                filesize = os.path.getsize('./queue/' + filename)
                client_socket.send(encrypt(f'{filename}:{filesize}'.encode(), encryption_key))

                progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True,unit_divisor=1008)
                with open('./queue/' + filename, "rb") as f:
                    while True:
                        # read the bytes from the file
                        bytes_read = f.read(1008)
                        if not bytes_read:
                            # file transmitting is done
                            os.remove('./queue/' + filename)
                            keep_alive = False
                            break
                        # we use sendall to assure transimission in
                        # busy networks
                        client_socket.send(encrypt(bytes_read, encryption_key))
                        # update the progress bar
                        progress.update(len(bytes_read))

            else:
                client_socket.send(encrypt('<nofile>'.encode(), encryption_key))
                keep_alive = False
        client_socket.close()
