import os
import json

# run the script in /valve/sprites folder

result = {}
for i in os.listdir(os.getcwd()):
    if i.endswith(".txt"):
        print(f"Found potential weapon txt file: {i}")
        with open(i, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            ammo_replacement_data = {}
            ammo_key = ""

            crosshair_replacement_data = {}
            crosshair_key = ""

            for line in lines:
                if 'ammo' in line:
                    if '1280' in line:
                        ammo_replacement_data['1280'] = " ".join(line.split()).split()
                    elif '2560' in line:
                        ammo_replacement_data['2560'] = " ".join(line.split()).split()
                    elif '640' in line:
                        ammo_key = " ".join(line.split())
                elif 'crosshair' in line:
                    if '1280' in line:
                        crosshair_replacement_data['1280'] = " ".join(line.split()).split()
                    elif '2560' in line:
                        crosshair_replacement_data['2560'] = " ".join(line.split()).split()
                    elif '640' in line:
                        crosshair_key = " ".join(line.split())

            if ammo_replacement_data != {}:
                result[ammo_key] = ammo_replacement_data

            if crosshair_replacement_data != {}:
                result[crosshair_key] = crosshair_replacement_data

with open("result.json", "w", encoding="utf-8") as json_file:
    json.dump(result, json_file, indent=4, ensure_ascii=False)