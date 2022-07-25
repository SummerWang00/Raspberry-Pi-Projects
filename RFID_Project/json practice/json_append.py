import json

from unicodedata import name
# from os import

filename = "C:\\Users\\xwang\\Documents\\repos\\Raspberry-Pi-Projects\\RFID_Project\\json practice\\name.json"
# dump file content into data.
def write_json(data: object, filename: str = filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def display_choices():
    print("Database for names!")
    print("(1) View Data")
    print("(2) Add Data")
    print("(3) Delete Data")
    print("(4) Edit Data")
    print("(5) Exit the program")

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

def add_person():  #name: str, id: int
    
    name = input("Please enter firstname: ")
    print(f"Firstname {name} added")

    while True:
        try:
            id = int(input("What is her/his ID#? "))
            break
        except:
            print("Error: Invalid number")

    print(f"{id} added.")
    print("It's the {} entry! Congrats!")   # try to access the item order number in json file to say this is the 4th person or something
    print(f"{name}'s information added! Type 'a' to add one more person, anything else to quit: ")
    adding = input("")
    if (adding == 'a'):
        add_person()
    else:
        print("Add no more.")
    print("Added")
    return name, id

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

# def edit_Person():
#     view_data()
#     new_data = []


# based on choice input, handles which function to execute. If error occurs, prompt for a new choice entry
def select_mode():
    while True:
        mode_choice = input("Type 'a'(lowercase) to add a person's information or 'd' to add: ")
        if (mode_choice == 'a'):
            add_person()
            break
        elif (mode_choice == 'd'):
            remove_person()
            break
        else:
            print("Error, please start over")
            select_mode()



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

#this is equal to main function
with open(filename) as json_file:
    data = json.load(json_file) # open the json file
    #select_mode()
    # Question: open file first?
    # Or, write a function to open file in different modes and pass a parameter to see
    # what mode to use? I'll figure out tomorrow morning.


    name, id = add_person()
    x = {"firstname": name, "ID#": id}
    #y = {"firstname": "Joseph", "age": 29, "ID#": 1823908214214}  # what's being added
    data["names"].append(x)

while (True):
    display_choices()
    choice = input("\nEnter Number:")
    if choice == "1":
        view_data()
        break
    elif choice == "2":
        add_person()
        break
    elif choice == "3":
        remove_person()
        break
    elif choice == "4":
        edit_Person()
        break
    elif choice == "5":
        break
    else:
        print("Nothing is selected, try again")

write_json(data)
