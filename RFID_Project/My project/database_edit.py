from enum import Enum
from unicodedata import name

import scanner_get_id.py

secs = 10
access = False
time_to_stop_scanning = 0  # every time scan() runs I want it to be in effect for 20 seconds
filename = "C:\\Users\\xwang\\Documents\\repos\\Raspberry-Pi-Projects\\RFID_Project\\My project\\name.json"
state: int = 0 # is it a good idea to define it here? Why? - good idea, because it'sd good practice to enter a default state at the beginning of a program

def add_person():
    # Need to figure out a way to add multiple people one after another without exiting this state
    state = safe_int_input("How do you want to add?\nEnter (1) to add through scanning ID, (2) to type in information manually:")
    if state == Admin_add_state.SCAN.value:
        # Question!!! Do you think it's better to set up the GPIO and scanner, splitting the set up code before solely scan function before prompting it's ready to scan, or to the way it is right now?
        print("Scanner set up...")
        int_id = scan()
        name = input("Please enter firstname: ")
        print(f"You entered:\nFirstname: {name} and ID#: {int_id}")
        confirm = input("Confirm your entry? Enter y to continue, n to start again")
        if confirm == 'y':
            add_to_database(name, int_ID)
            print("Added!")
        print(f"Type 'a' to add one more person, anything else to quit: ")
        adding = input("")
        if (adding == 'a'):
            add_person()
        else:
            print("Add no more.")

    elif state == Admin_add_state.TYPE.value:
        print("Enter data to add to database")
        name = input("Name: ")
        int_ID = int(input("ID:"))
        print(f"You entered:\nFirstname: {name} and ID#: {int_id}")
        confirm = input("Confirm your entry? Enter y to continue, n to start again")
        if confirm == 'y':
            add_to_database(name, int_ID)
            print("Added!")

    elif state == Admin_add_state.SELECT.value:
        print("You chose to select")

    else:
        print("invalid input. Try again...")
    
    #if program comes here... state should change? or not.

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

def safe_int_input(prompt: str):  # If anything entered isn't an int, ask user to re-enter
    while True:
        try:
            result = int(input(prompt))
            break
        except ValueError:
            print("Numbers only please!")
    return result

def init_choices():
    print("Database for names! Enter respective numbers to proceed")
    print("(0) Admin Mode - can access and modify database(Valid account and password needed)")
    print("(1) Normal Mode - start scanning for ID")

def admin_choices():
    print("What do you want to do? \nEnter (1) to add a person, (2) to remove a person.")

def normal_prompt():
    print("Starting normal mode, waiting to scan ID...")

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
def scan():  # returns ID number in int
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
                # flush, so that each dot in the buffer is flushed right after it enters the buffer
                print('.', end="", flush=True) 
                uid = pn532.read_passive_target(timeout=1)
                ID_undetected_time = ID_undetected_time + 1  # only scan every one second.

                if ID_undetected_time == secs: #ANY IDEA WHAT to call this variable
                    ID_undetected_time = 0
                    print("Where's the card? Still waiting~")

                if uid is None:
                    continue
                
                int_uid = int(uid.hex(), 16)
                print('Found card with UID:', int_uid) # prints out card ID in int

# dunno what to do here i was gonna do something
                if 
                break
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

def add_to_database(name: str, ID: int):  # this goes inside of add_person to add inputs into database
    with open(filename) as json_file:
        data = json.load(json_file) # open the json file
        #select_mode()
        # Question: open file first then wait for parameters to modify file
        # Or, write a function to open file in different modes and pass a parameter 'w' or 'r'
        x = {"firstname": name, "ID#": ID}
        data["names"].append(x)
        write_json(data)

def write_json(data: object, filename: str = filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
  
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
    ID = 3

class Admin_edit_state(Enum):
    SELECT = 0
    SCAN = 1
    NAME = 2
    ID = 3   # ask for manual ID input

# this acts like main function in C
while True:
    init_choices()  # with this function, I don't think I need select state. If you put in the select state, how do you do that? Do you need a prompt to put in 0 to enter select state.
    state = safe_int_input("\nEnter Number:")
    # check if valid before assigning
    # make states
    if state == State.ADMIN:
        admin_choices()
        state = safe_int_input()
        if state == Admin_state.ADD.value:
            add_person()
            state = 0
            continue
        elif state == Admin_state.REMOVE.value:
            remove_person()
            state = 0
            continue
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

    # Normal mode: scanner keeps running until the stop action - pressing a button or key in a key. 
    elif state == State.NORMAL:
        while True:
            normal_prompt()
            int_id = scan()  #scan and output id
            access = check_access(int_id)
            ''' if access == True:
                    #green LED lights up and actuator contracts
                else:
                    red LED lights up and buzzer buzzs continuously
            '''


    else:
        print("Invalid input, enter a number from the available choices again")
