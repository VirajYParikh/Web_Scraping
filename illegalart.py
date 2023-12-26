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

link = config.get("illegalart", "link")


def data_illegalart(link):

    response = requests.get(link)

    if response.status_code == 200:
        # Get the HTML content
        html_content = response.content

        # Parse the html content
        soup = BeautifulSoup(html_content, "html.parser")

        artists = []
        # Getting the artist hrefs from the page
        artist_links = soup.find_all("div", class_="artist")
        
        for artist_link in artist_links:
            artist_name = artist_link.find("a").get_text(strip=True)
            artist_info = {"ArtistName": artist_name}
            artists.append(artist_info)
            # artists.append(process_artist(href))
        print(artists)

        # Saving the data to a json file
        with open('../NEW_DATA/illegalart.json', 'w') as f:
            json.dump(artists, f, indent=4, sort_keys=True)
        


def main():
    start_ = time.time()
    data_illegalart(link)
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
