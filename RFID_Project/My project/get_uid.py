"""
This example shows connecting to the PN532 with I2C (requires clock
stretching support), SPI, or UART. SPI is best, it uses the most pins but
is the most reliable and universally supported.
After initialization, try waving various 13.56MHz RFID cards over it!
"""

from pn532 import *
from unicodedata import name

import RPi.GPIO as GPIO
import json
import time

file = "name_ID_data.json"

# global variables
secs = 10
access = False

if __name__ == '__main__':
    try:
        # Uncomment corresponding lines below to configure interface, only keep one line uncommented at a time.
        # Jumpter configuration -
        # SPI 1 0   I2C 0 1    UART 0 0
        #     1 1       1 1         1 1
        #     0 1       1 0         1 1
        # pn532 = PN532_SPI(debug=False, reset=20, cs=4)
        pn532 = PN532_I2C(debug=False, reset=20, req=16)
        #pn532 = PN532_UART(debug=False, reset=20)

        # SET UP

        ic, ver, rev, support = pn532.get_firmware_version()
        print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

        # Configure PN532 to communicate with MiFare cards
        pn532.SAM_configuration()

        #Start of program, choose mode
        input('Enter "r" to for ID reader mode and "e" to add or remove a person from database: ')
        print('Waiting for RFID/NFC card...')
        ID_undetected_time: int = 0
        while True:
            # Check if ID_undetected_time card is available to read
            # read_passive_target get the uid and store it in variable uid.

            # The message doesn't print after so long idk why???
            # It's the print statemenet's fault. Buffer doesn't flush immediately
            # I want to print "Still waiting" after 1o timeouts. Every  loop

            if ID_undetected_time == secs:
                ID_undetected_time = 0
                print("Where's the card? Still waiting~")

            print('.', end="", flush=True)  #moved from below UID code
            uid = pn532.read_passive_target(timeout=1)

            ID_undetected_time = ID_undetected_time + 1

            # Try again if no card is available. while loop starts over without continuing print()
            if uid is None:
                continue

            # Display UID information, reset counter
            # print('Found card with UID:', [hex(i) for i in uid])    #i is each digit in a hex number, from example
            # print('Found card with UID:', uid.hex())                #.hex() conbines uid together

            #int_uid stores the reader input to compare with database
            int_uid = int(uid.hex(), 16)
            print('Found card with UID:', int_uid) # converts hex number into 16-bit int

            # print(type(uid))
            ID_undetected_time = 0

            # print('Found card with UID:', [uid.decode()])   #prints the same as hex(i)
            # print(type((uid).decode()))  #this returned class 'bytes', so it is ID_undetected_time byte object? Using the function byte() can turn ID_undetected_time list/number into ID_undetected_time byte object
                                            #this is very weird, error message 'utf-8' codec can't decode byte 0xb1 in position 2: invalid start byte
            #imagine I open the json database file here
            # and then store that into

            '''
            logic:
            Compare UID to existing database
            access = False
            for ID in <database ID data>:   #check through every single name and ID pair to find matches
                if ID == int_id:
                    print("Access allowed for <name>")
                else:
                    print("Access denied")
                    access = false
                if access = true:
                    access = false
            '''

            with open (file, encoding="utf-8",) as json_file: #encoding="utf-8"
                data = json.load(json_file)
                name_data = (data["names"])       #make name_data into a list of individual dictionary\

                for i in name_data:
                    name = (i["name"])   # adding end="" get rid of the audo new line character
                    ID = (i["ID#"])
                    if int_uid == ID:
                        # Green LED light up
                        access = True
                        print(f"This is {name}'s card, access granted, door opened", end="\n\n")
                        break
                    else:
                        continue

                if access == False:
                    print("I don't know you, access denied!")  # when this line is indented it turns grey

            access = False
            time.sleep(1)

    except Exception as e:
        print(e)

    finally:
        GPIO.cleanup()
