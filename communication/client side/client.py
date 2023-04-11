import socket
import rsa
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import tqdm


def encrypt(data, encryption_key):
    cipher = AES.new(encryption_key, AES.MODE_EAX)
    return cipher.nonce + cipher.encrypt(data)


def decrypt(data, encryption_key):
    cipher = AES.new(encryption_key, AES.MODE_EAX, nonce=data[0:16])
    return cipher.decrypt(data[16:])


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
    client_socket.send(rsa.encrypt(encryption_key, temp_key))
    while (keep_alive):
        data = decrypt(client_socket.recv(1024), encryption_key).decode()
        print(data)
        if data != '<nofile>':
            filename, filesize = data.split(':')
            filesize = int(filesize)

            progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1008)
            with open(filename, "wb") as f:
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
        keep_alive = False
