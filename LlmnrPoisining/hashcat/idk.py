import multiprocessing
from multiprocessing import Process
from scapy.all import *
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.gssapi import GSSAPI_BLOB, SPNEGO_negToken, SPNEGO_negTokenResp
from scapy.layers.llmnr import *
from scapy.layers.inet import UDP, IP, ICMP, TCP
import socket
from scapy.layers.netbios import NBNSQueryResponse, NBNSQueryRequest, NBTSession, NBNS_ADD_ENTRY, NBNSHeader
from scapy.layers.ntlm import NTLM_NEGOTIATE, NTLM_RESPONSE, NTLMv2_RESPONSE
from scapy.layers.smb import SMBNegotiate_Request, SMB_Header
from scapy.layers.smb2 import SMB2_Header, SMB2_Negotiate_Protocol_Request, SMB2_Negotiate_Protocol_Response
import time

hostname = socket.gethostname()
ips = socket.gethostbyname(hostname)
print("Your Computer Name is:" + hostname)
print("Your Computer IP Address is:" + ips)


def func(pipe):
    pipe.send('hi')


def de(packet):
    # if IP in packet and UDP in packet and packet[UDP].sport == 5353 and packet[
    #     UDP].dport == 5353 and DNS in packet and DNSQR in packet and packet[DNSQR].qtype == 1:
    #     packet.show()
    #     response = IP(dst=packet[IP].src) / UDP(sport=5353, dport=5353) / DNS(qdcount=0, qd=packet[DNSQR],
    #                                                                           an=DNSRR(rrname=packet[DNSQR].qname,
    #                                                                                    type=1, rdata=ips))
    packet.show()



if __name__ == '__main__':

    sniff(lfilter=de)
    # print('start' + str(os.stat('cracked.txt').st_size))
    # if os.stat('cracked.txt').st_size == 0:
    #     print("empty")
    #
    # else:
    #     with open(r'cracked.txt', 'r') as file:
    #         print(file.read())
    # print('end')
    # packets = sniff(lfilter=func, count=5)
    # print(packets)
    # for x in packets:
    #     print(x)
    # for x in packets:
    #     if SMB2_Header in x:
    #         print(x[SMB2_Header])
    #     try:
    #         x.show()
    #     except:
    #         print('exception-' + str(x))
    # packet = LLMNRQuery()
    # packet.show()
    # packet = TCP(options=(SMB2_Header() / SMB2_Negotiate_Protocol_Request()))
    # packet.show()
    # packet = SMB2_Header() / SMB2_Negotiate_Protocol_Response()
    # packet.show()
    # packet = SMB2_Header(HeaderLength=64, CreditCharge=1, Command=1, Flags=1, CreditsRequested=1)
    # packet.show()
    # packet = IP(src='192.168.68.115', dst='192.168.68.118') / TCP(sport=445, dport=1854,
    #                                                               seq=1,
    #                                                               ack=1,
    #                                                               flags='PA') / NBTSession(TYPE=1) / SMB2_Header(
    #     HeaderLength=64,
    #     CreditCharge=0,
    #     Command=0,
    #     Flags=1,
    #     CreditsRequested=1) / SMB2_Negotiate_Protocol_Request(
    #     StructureSize=65,
    #     SecurityMode=1,
    #     Dialect=0x02ff,
    #     NegociateCount=0,
    #     Capabilities=0x00000007,
    #     MaxTransactionSize=8388608,
    #     MaxReadSize=8388608,
    #     MaxWriteSize=8388608,
    #     ServerGUID='0ba1264d-898c-412a-7867-0fba3964a102')
    # packet[NBTSession].LENGTH = len(
    #     packet[NBTSession]) + len(packet[SMB2_Negociate_Protocol_Response_Header]) + len(packet[SMB2_Header])
    # packet.show()
    # send(packet)
