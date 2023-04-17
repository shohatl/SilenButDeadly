import os
import subprocess
import time

if __name__ == '__main__':
    print('yo boiiiii')
    print('trolololo')
    f = open('./hi.txt', 'w')
    f.write('works')
    f.close()
    print('dam fam')
    t = time.time()
    while (time.time() - t < 5):
        time.sleep(1)
        print(time.time() - t)
        pass
    os.system('start 9.jpg')

    # subprocess.run(['python', './LlmnrPoisining/hashcat/sniffCredentials.py'])

    # subprocess.run(['python', 'communication/client side/client.py'])
