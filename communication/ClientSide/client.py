import os
import time
import FileTransfer


def main():
    keep_alive = True
    is_script = True
    while (keep_alive):
        time.sleep(0.1)
        client_socket, encryption_key = FileTransfer.initiate()
        print('connected')
        if (os.listdir('./output')):
            filename = os.listdir('./output')[0]
            if (filename == 'default.txt'):
                print('here')
                client_socket.send(FileTransfer.encrypt('<doutput>'.encode(), encryption_key))
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
            client_socket.send(FileTransfer.encrypt('<update>'.encode(), encryption_key))
            keep_alive = False
            client_socket.close()
        print('done')


if __name__ == '__main__':
    main()
