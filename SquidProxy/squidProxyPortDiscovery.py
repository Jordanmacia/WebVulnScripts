#!/usr/bin/python3

import sys, signal, requests

def def_handler(sig, frame):
    print("\n\n[!] Exiting...\n")
    sys.exit(1)


# Ctrl+C 
signal.signal(signal.SIGINT, def_handler)

main_url = "http://127.0.0.1"
squid_proxy = {'http': 'http://192.168.71.131:3128'}


def portDiscovery():

    common_tcp_port= {21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080, 8443, 8888, 5900, 6666, 6667, 6668, 6669, 7000, 10000, 32768, 32769, 32770, 32771, 32772, 32773, 32774, 32775, 32776, 32777, 32778, 32779, 49152, 49153, 49154, 49155, 49156, 49157, 49158, 49159, 49160, 49161, 49162}

    for tcp_port in common_tcp_port:
        r = requests.get(main_url + ':' + str(tcp_port), proxies=squid_proxy)

        if r.status_code != 503:
            print("\n[+] Port " + str(tcp_port) + "- OPEN")

if __name__ == '__main__':

    portDiscovery()
