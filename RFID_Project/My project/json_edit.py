from pn532 import *
from unicodedata import name

import RPi.GPIO as GPIO
import time
import json
from enum import Enum
from unicodedata import name

secs = 10
access = False
filename = "C:\\Users\\xwang\\Documents\\repos\\Raspberry-Pi-Projects\\RFID_Project\\My project\\name.json"
state: int

class Init_state(Enum):
    SELECT = 0
    ADMIN = 1
    NORMAL = 2

    # ADD = 2
    # REMOVE = 3
    # EDIT = 4
    # DISPLAY = 5

    # ALLOW = 10

    # TYPE = 20
    # SCAN = 21

class Admin_state(Enum):
    SELECT = 0
    ADD = 1
    REMOVE = 2
    EDIT = 3
    DISPLAY = 4

class Normal_state(Enum):
    LOCKED = 0
    UNLOCKED = 1

class Admin_add_state(Enum):  # what is select for? Why did you say it's good to have, I thought when you enter add state user will be prompted to select
    SELECT = 0
    SCAN = 1
    TYPE = 2

class Admin_remove_state(Enum):
    SELECT = 0
    SCAN = 1
    NAME = 2
    TYPE = 3

def add_person():  #name: str, int_uid: int
    name = input("Please enter firstname: ")
    print(f"Firstname {name} added")

    while True:
        try:
            int_uid = int(input("What is her/his ID#? "))
            break
        except:
            print("Error: Invalid number")

    print(f"{int_uid} added.")
    print("It's the {} entry! Congrats!")   # try to access the item order number in json file to say this is the 4th person or something
    print(f"{name}'s information added! Type 'a' to add one more person, anything else to quit: ")
    adding = input("")
    if (adding == 'a'):
        add_person()
    else:
        print("Add no more.")
    print("Added")
    return name, int_uid

# deletes a person's data, find the person through unique identifiers, could be name or ID.
def remove_person():
    #view_data()
    new_data = []
    # file opening
    with open(filename, "r") as f:
        temp = json.load(f)
        data_length = len(temp) - 1
    print("which index number would you like to delete?")
    option = input(f"Select a number in 0-{data_length}")
    i = 0
    # find the index the user wants to delete
    for entry in temp:
        if i == int(option):
            pass
            i = i+1
        else:
            new_data.append(entry)
            i = i+1
    with open(filename, "w") as f:
        json.dump(new_data, f, indent=4) 
            
    print("removed")

def edit_person():
    view_data()
    new_data = []

# Need to figure out why I needed this... I think I saw it somewhere
# Resolved, it was from StackOverflow

#this is equal to main function
with open(filename) as json_file:
    data = json.load(json_file) # open the json file
    #select_mode()
    # Question: open file first?
    # Or, write a function to open file in different modes and pass a parameter to see
    # what mode to use? I'll figure out tomorrow morning.
    name, int_uid = add_person()
    x = {"firstname": name, "ID#": int_uid}
    data["names"].append(x)

def init_choices():
    print("Database for names! Enter respective numbers to proceed")
    print("(0) Admin Mode - can access and modify database(Valid account and password needed)")
    print("(1) Normal Mode - start scanning for ID")

def admin_choices():
    print("What do you want to do? \nEnter (1) to add a person, (2) to remove a person.")

while (True):
    init_choices()  # with this function, I don't think I need select state. If you put in the select state, how do you do that? Do you need a prompt to put in 0 to enter select state.
    state = safe_int_input("\nEnter Number:")

    # make states
    if state == State.ADMIN:
        admin_choices()
        state = safe_int_input()
        if state == Admin_state.ADD.value:
            add_person()
            state = 0

        elif state == Admin_state.REMOVE.value:
            remove_person()
            state = 0
            break
        elif state == Admin_state.EDIT.value:
            edit_person()
            state = 0
            continue
        else:
            print("Invalid input, enter again")
            break

            # how_to_add = safe_int_input("Enter 0 to add by scanning, or 1 to type ID manually:")
            # if how_to_add == 0:
            #     int_id = scan()  #I need to write scan function to scan using ID. 
            # #   check_access(int_id)  I forgot why I needed to check access
            # elif how_to_add == 1:
            #     #insert logic to type ID manually
            #     print("Selected to add ")
            #     int_id = safe_int_input("please enter your 9-digit ID:")

    elif state == State.NORMAL:
        int_id = scan()  #scan and output id
        access = check_access(int_id)
        ''' if access == True:
                #green LED lights up and actuator contracts
            else:
                red LED lights up and buzzer buzzs continuously
        '''

    else:
        print("Invalid input, enter a number from the available choices again")

write_json(data)

def safe_int_input(prompt):  # If anything entered isn't an int, ask user to re-enter
    while True:
        try:
            result = int(input(prompt))
            break
        except ValueError:
            print("Numbers only please!")
    return result

def view_data():
    with open(filename, "r") as f:
        temp = json.load(f)
        i = 0
        for entry in temp:
            name = entry["firstname"]
            int_uid = entry["ID#"]
            print(f"Index#: {i}")
            print(f"Name #{i+1} is: {name}")
            print(f"ID#: {int_uid}", end="\n\n")
            i = i+1

# dump file content into data.
def write_json(data: object, filename: str = filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def scan():  ## returns ID number in int
    if __name__ == '__main__':
        try:
            # SET UP
            pn532 = PN532_I2C(debug=False, reset=20, req=16)
            ic, ver, rev, support = pn532.get_firmware_version()
            print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

            # Configure PN532 to communicate with MiFare cards
            pn532.SAM_configuration()
            print('Waiting for RFID/NFC card...')
            ID_undetected_time: int = 0
            while True:
                if ID_undetected_time == secs:
                    ID_undetected_time = 0
                    print("Where's the card? Still waiting~")
                print('.', end="", flush=True) #flush so that each dot in the buffer is flushed right after it enters the buffer
                uid = pn532.read_passive_target(timeout=1)
                ID_undetected_time = ID_undetected_time + 1  # only scan every one second.

                if uid is None:
                    continue
                int_uid = int(uid.hex(), 16)
                print('Found card with UID:', int_uid) # prints out card ID in int

    # returns integer ID number
        except Exception as e:
            print(e)

        finally:
            GPIO.cleanup()
    return int_uid

def check_access(int_uid):
    access = False
    with open (file, encoding="utf-8",) as json_file: #encoding="utf-8"
        data = json.load(json_file)
        name_data = (data["names"])       #make name_data into a list of individual dictionary\

        for i in name_data:
            name = (i["name"])   # adding end="" get rid of the audo new line character
            ID = (i["ID#"])
            if int_uid == ID:    # ID exist in database
                access = True
                print(f"This is {name}'s card, access granted, door opened", end="\n\n")
                break
            else:
                continue

    time.sleep(1)
    return access