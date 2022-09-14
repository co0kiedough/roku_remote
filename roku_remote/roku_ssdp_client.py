import os
import socket
import sys
import time
import threading
import re
class Client(threading.Thread):
    # 30 seconds for search_interval
    SEARCH_INTERVAL = 5
    BCAST_IP = '239.255.255.250'
    BCAST_PORT = 1900

    def __init__(self):
        threading.Thread.__init__(self)
        self.interrupted = False
        
    def run(self):
        self.keep_search()
    
    def stop(self):
        self.interrupted = True
        print("upnp client stop")

    def keep_search(self):
        '''
        run search function every SEARCH_INTERVAL
        '''
        try:
            while True:
                self.search()
                for x in range(self.SEARCH_INTERVAL):
                    time.sleep(1)
                    if self.interrupted:
                        return
        except Exception as e:
            print('Error in upnp client keep search %s', e)

    def search(self):
        '''
        broadcast SSDP DISCOVER message to LAN network
        filter our protocal and add to network
        '''
        ssdpRequest = "M-SEARCH * HTTP/1.1\r\n" + \
        "HOST: 239.255.255.250:1900\r\n" + \
        "Man: \"ssdp:discover\"\r\n" + \
        "MX: 5\r\n" + \
        "ST: roku:ecp\r\n" + \
        "\r\n";
        socket.setdefaulttimeout(100)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        sock.sendto(ssdpRequest.encode('ASCII'), ("239.255.255.250".encode('ASCII'), 1900))
        while True:
            
            resp = sock.recv(1024)
            sresp = resp.decode()
            print(sresp)
#print("Matches")
# matchObj = re.match(r'.*USN: uuid:roku:ecp:([\w\d]{12}).*LOCATION: (http://.*/).*', sresp)
# print (matchObj)
#             