import json

filename = "edited_name.json"

def write_json(data: object, filename: str="name.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

with open("name.json") as json_file:  #open current json file
    data = json.load(json_file)       #store json file as python object in data
    temp = data["names"]              #get whatever that is under names into temp
    y = {"firstname": "new person", "ID#": 45} 
    temp.append(y)                    #get

write_json(data)
