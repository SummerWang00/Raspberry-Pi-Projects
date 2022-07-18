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

file = "name_ID_data.json"

if __name__ == '__main__':
    try:
        # pn532 = PN532_SPI(debug=False, reset=20, cs=4)
        pn532 = PN532_I2C(debug=False, reset=20, req=16)
        #pn532 = PN532_UART(debug=False, reset=20)

        ic, ver, rev, support = pn532.get_firmware_version()
        print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

        # Configure PN532 to communicate with MiFare cards
        pn532.SAM_configuration()

        print('Waiting for RFID/NFC card...')
        count_wait_message: int = 0
        while True:
            # Check if count_wait_message card is available to read
            # read_passive_target get the uid and store it in variable uid.
           
            # The message doesn't print after so long idk why???
            # I want to print "Still waiting" after 1o timeouts. Every 10 loops 
 
            if count_wait_message == 5:
                count_wait_message = 0
                print("Where's the card? Still waiting~")

            print('.', end="")  #moved from below UID code
            uid = pn532.read_passive_target(timeout=1)
             
            count_wait_message = count_wait_message+1

            # Try again if no card is available.
            if uid is None:
                continue
            print('Found card with UID:', [hex(i) for i in uid]) # i is each digit
            # print(uid[0])
            # print('Found card with UID:', [uid.decode()])   #prints the same as hex(i)
            print('Found card with UID:', uid.hex())     #.hex() conbines uid together
            
            int_uid = int(uid.hex(), 16)
            print('Found card with UID:', int_uid) # converts hex number into 16-bit int

            print(type(uid))
            print("")
            count_wait_message = 0

            # print(type((uid).decode()))  #this returned class 'bytes', so it is count_wait_message byte object? Using the function byte() can turn count_wait_message list/number into count_wait_message byte object
                                            #this is very weird, error message 'utf-8' codec can't decode byte 0xb1 in position 2: invalid start byte
            #imagine I open the json database file here
            # and then store that into 

            '''
            logic:
            Compare UID to existing database
            access = false
            for ID in <database ID data>:   #check through every single name and ID pair to find matches
                if ID == int_id:
                    print("Access allowed for <name>")
                else:
                    print("Access denied")
                    access = false
                if access = true:
                    access = false
            '''

    except Exception as e:
        print(e)
      
    finally:
        GPIO.cleanup()
