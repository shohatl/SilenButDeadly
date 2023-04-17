import os
import time
import FileTransfer


if __name__ == '__main__':
    server_ip = '127.0.0.1'
    keep_alive = True
    is_script = True
    while (keep_alive):
        client_socket, encryption_key = FileTransfer.initiate(server_ip, 786)
        print('connected')
        if (os.listdir('./output')):
            filename = os.listdir('./output')[0]
            if (filename == 'default.txt'):
                pass
            else:
                client_socket.send(FileTransfer.encrypt('<newoutput>'.encode(), encryption_key))
                time.sleep(0.1)
                FileTransfer.send(client_socket, encryption_key, filename, './output/')
                os.remove('./output/' + filename)

        elif (not os.listdir('./script') and is_script):
            print('need new script')
            client_socket.send(FileTransfer.encrypt('<newscript>'.encode(), encryption_key))
            data = FileTransfer.decrypt(client_socket.recv(1024), encryption_key).decode()
            print(data)
            if data != '<nofile>':
                FileTransfer.receive(client_socket, encryption_key, data, './script/')
            else:
                is_script = False
        else:
            client_socket.send(FileTransfer.encrypt('update'.encode(), encryption_key))
            keep_alive = False
        client_socket.close()
        print('done')
