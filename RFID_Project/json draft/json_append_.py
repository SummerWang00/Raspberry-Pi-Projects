import json

filename = "name.json"


# open file, and dump file content into data.
def write_json(data: object, filename: str = filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


with open(filename) as json_file:
    data = json.load(json_file) # opsn the json fil
    y = {"firstname": "Joseph", "age": 29, "ID#": 1823908214214}  # what's being added
    data["names"].append(y)                                       # actually adding
#   name = input("Please Enter")

write_json(data)