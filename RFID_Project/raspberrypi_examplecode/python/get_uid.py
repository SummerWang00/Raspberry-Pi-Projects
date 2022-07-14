"""
This example shows connecting to the PN532 with I2C (requires clock
stretching support), SPI, or UART. SPI is best, it uses the most pins but
is the most reliable and universally supported.
After initialization, try waving various 13.56MHz RFID cards over it!
"""

from unicodedata import name
import RPi.GPIO as GPIO

from pn532 import *


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
        while True:
            # Check if a card is available to read
            # read_passive_target get the uid and store it in variable uid.
            uid = pn532.read_passive_target(timeout=5)
            print('.', end="")
            # Try again if no card is available.
            if uid is None:
                continue
            print('Found card with UID:', [hex(i) for i in uid])
            # print(uid[0])
            print(type(uid))
            # print('Found card with UID:', [uid.decode()])   #prints the same as hex(i)
            print('Found card with UID:', uid.hex())     #prints weird number starting with b'
            
            print('Found card with UID:', int(uid.hex(), 16))
            # print(type((uid).decode()))  #this returned class 'bytes', so it is a byte object? Using the function byte() can turn a list/number into a byte object
                                            #this is very weird, error message 'utf-8' codec can't decode byte 0xb1 in position 2: invalid start byte
            #imagine I open the json database file here
            # and then store that into 
            # for i in name_data:hvjhvj
              
    
    except Exception as e:
        print(e)
      
    finally:
        GPIO.cleanup()
