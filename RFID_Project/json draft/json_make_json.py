import json

File = "name.json"

def write_json(data: object, filename: str="02_new_name_data.json"):   #File name to write to
    with open(filename, "w") as f:           # things
        json.dump(data, f, indent=4)       #dump function takes data and makes it into a json File

# with open(File, "r") as json_file:
#     data = json.load(json_file)
#     write_json(data)

data ={"names":[
    {"name": "Summer", "ID#": '0x32 0xe 0xb1 0x3'},
{"name": "Julie", "ID#": '0x4d 0xf9 0xb1 0x3'},
{"name": "Hi", "ID#": '0xa4 0x70 0xb1 0x3'}
]}
write_json(data)