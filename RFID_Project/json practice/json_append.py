import json
# from os import

filename = "name.json"
# dump file content into data.
def write_json(data: object, filename: str = filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def add_Person():
    print("Added")

def remove_Person():
    print("removed")

def select_mode():
    mode_choice = input("Type 'a'(lowercase) to add a person's information or 'd' to add ")
    if (mode_choice == 'a'):
        add_Person()
    elif (mode_choice == 'd'):
        remove_Person()
    else:
        print("Error, please start over")
        select_mode()

with open(filename) as json_file:
    data = json.load(json_file) # open the json file

    


    y = {"firstname": "Joseph", "age": 29, "ID#": 1823908214214}  # what's being added
    data["names"].append(y)

