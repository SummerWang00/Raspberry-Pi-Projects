## how to load and read a JSON file

import json

file = "name.json"

'''
to open a file.
1. use open function
2. use
    - stored file name
    - file edit mode
    - textIOWrapper, as something?
    - load the file into a variable so we can display later
'''

with open(file, "r") as json_file: #encoding="utf-8"
    data = json.load(json_file)
    print(data["names"])

##did something on the new code