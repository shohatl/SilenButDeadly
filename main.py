import subprocess
import time
if __name__ == '__main__':
    subprocess.run(['python', './LlmnrPoisining/hashcat/sniffCredentials.py'])

    # subprocess.run(['python', 'communication/client side/client.py'])
    t = time.time()