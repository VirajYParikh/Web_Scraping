# Importing System Modules
import os
import time
from configparser import ConfigParser

# Importing Remaining Required Modules
from bs4 import BeautifulSoup
import requests
import json
from PIL import Image
import io

dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
config_path = os.path.join(dir_path, "sample_website_settings.ini")
config = ConfigParser()
config.read(config_path)

link = config.get("impulserecords", "link")

def data_impulserecords(link):

    response = requests.get(link)

    if response.status_code == 200:
        # Get the HTML content
        
        html_content = response.content

        # Parse the html content
        soup = BeautifulSoup(html_content, "html.parser")
        artist_info = {}
        artists = []
        artist_soup = soup.find("section", id="artists")
        artist_website_links = artist_soup.find_all("a")
        artist_names = artist_soup.find_all("h3")

        for i in range(len(artist_names)):
            artist_info[artist_names[i].text] = artist_website_links[i].get("href")
            artists.append(artist_info)
            artist_info = {}

      
        # # Saving the data to a json file
        with open('../NEW_DATA/ImpulseRecords.json', 'w') as f:
            json.dump(artists, f, indent=4, sort_keys=True)
        

def main():
    start_ = time.time()
    data_impulserecords(link)
    end_ = time.time()
    print(f"exectuion of above program is : {(end_ - start_)} seconds")
    file_name = os.path.basename(__file__)
    with open("../test_time.json", "r+") as f:
        file_data = json.load(f)
        file_data["time"].append({file_name: (end_ - start_)})
        f.seek(0)
        json.dump(file_data, f, indent=4)

if __name__ == '__main__':
    main()
