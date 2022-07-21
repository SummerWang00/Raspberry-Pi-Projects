import json
from unicodedata import name
# from os import

filename = "C:\\Users\\xwang\\Documents\\repos\\Raspberry-Pi-Projects\\RFID_Project\\json practice\\name.json"
# dump file content into data.
def write_json(data: object, filename: str = filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def add_Person():  #name: str, id: int
    name = input("Please enter firstname: ")
    print(f"Firstname {name} added")

    while True:
        try:
            id = int(input("What is her/his ID#? "))
            break
        except:
            print("Error: Invalid number")

    print(f"{id} added.")
    print("It's the 3rd entry! Congrats!")
    print(f"{name}'s information added! Type 'a' to add one more person, anything else to quit: ")
    adding = input("")
    if (adding == 'a'):
        add_Person()
    else:
        print("Add no more.")
    print("Added")
    return name, id

def remove_Person():
    view_data()
    new_data = []
    with open(filename, "r") as f:
        temp = json.load(f)
        data_length = len(temp) - 1
    print("which index number would you like to delete?")
    option = input(f"Select a number in 0-{data_length}")
    i = 0
    for entry in temp:
        if i == int(option):
            pass
            i = i+1
        else:
            
    print("removed")

def view_data():
    with open(filename, "r") as f:
        temp = json.load(f)
        i = 0
        for entry in temp:
            name = entry["firstname"]
            id = entry["ID#"]
            print(f"Index#: {i}")
            print(f"Name #{i+1} is: {name}")
            print(f"ID#: {id}", end="\n\n")
            i = i+1

def select_mode():
    while True:
        mode_choice = input("Type 'a'(lowercase) to add a person's information or 'd' to add: ")
        if (mode_choice == 'a'):
            add_Person()
            break
        elif (mode_choice == 'd'):
            remove_Person()
            break
        else:
            print("Error, please start over")
            select_mode()

with open(filename) as json_file:
    data = json.load(json_file) # open the json file
    #select_mode()
    # name = "Hailie"
    # id = "123907"
    name, id = add_Person()
    x = {"firstname": name, "ID#": id}
    #y = {"firstname": "Joseph", "age": 29, "ID#": 1823908214214}  # what's being added
    data["names"].append(x)

write_json(data)

def safe_int_input():
    num_retries = 3
    for attempt_no in range(num_retries):
        try:
            return int(input("Importance:\n\t1: High\n\t2: Normal\n\t3: Low"))
        except ValueError as error:
            if attempt_no < (num_retries - 1):
                print("Error: Invalid number")
            else:
                raise error