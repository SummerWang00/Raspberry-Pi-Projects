import json
from unicodedata import name

filename = "C:\\Users\\xwang\\Documents\\repos\\Raspberry-Pi-Projects\\RFID_Project\\json practice\\name.json"

def add_to_database(name: str, ID: int):  # this goes inside of add_person to add inputs into database
    with open(filename) as json_file:
        data = json.load(json_file) # open the json file
        x = {"firstname": name, "ID#": ID}
        data["names"].append(x)
        write_json(data)

def write_json(data: object, filename: str = filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

while True:
    print("Enter data to add to database")
    name = input("Name: ")
    int_ID = int(input("ID:"))
    add_to_database(name, int_ID)
    print("Added!")
