import os
import json

directory = '/Users/virajparikh/viraj_work/Octavate/Latest_Octavate/4-additional-record-label-scraping/NEW_DATA'
output_file = '/Users/virajparikh/viraj_work/Octavate/Latest_Octavate/4-additional-record-label-scraping/NEW_DATA/combined_data.json'

json_files = [file for file in os.listdir(directory) if file.endswith('.json')]


combined_data = []

for file in json_files:
    file_path = os.path.join(directory, file)
    
    try: 
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            combined_data.append(data)
    except json.JSONDecodeError as e:
        print("f:Error decoding json {file}. Details: {e}")
        continue
        

with open(output_file, 'w') as json_output:
    json.dump(combined_data, json_output)

    

