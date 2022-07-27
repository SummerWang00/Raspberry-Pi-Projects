## how to load and read a JSON file

import json

file = "name_ID_data.json"

'''
to open a file.
1. use open function
2. use
    - stored file name
    - file edit mode
    - textIOWrapper, as something?
    - load the file into a variable so we can display later
'''

with open (file, encoding="utf-8",) as json_file: #encoding="utf-8"
    data = json.load(json_file)
    name_data = (data["names"])       #make name_data into a list of individual dictionary
    for i in name_data:
        name = (i["name"])   # adding end="" get rid of the audo new line character
        ID = (i["ID#"])
        print (f"{name}'s ID# is {ID}")
##did something on the new code

'''
Scrap code1. 
for i in name_data:
                    name = (i["name"])   # adding end="" get rid of the audo new line character
                    ID = (i["ID#"])
                    if int_uid == ID:
                        # Green LED light up
                        print(f"{name} has access, door opened")
                    else:
                        print("Access denied!")
                    This would print something for every comparison with database data, whether the card has access or not.
                    I want it to print one message only when program figures out a person have access AT THE END. 



'''