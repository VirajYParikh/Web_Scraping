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

link = config.get("idolrecords", "link")

def process_artist(link, href):
    artist_url = link + "artists/index.php?" + href
    artist_response = requests.get(artist_url)
    # If the correct url is hit
    artist_info = {}
    try:
        if artist_response.status_code == 200:
            artist_html_content = artist_response.content
            artist_soup = BeautifulSoup(artist_html_content, "html.parser")
            try:
                artist_name = artist_soup.find('span', class_='headlinetitle').get_text(strip=True)
                artist_info = {"ArtistName": artist_name}

                artist_links_location = artist_soup.find("div", id="footer-center")
                artist_social_links = artist_links_location.find_all("a", class_="nav-footer")

                for artist_social_link in artist_social_links:
                    socialType = artist_social_link.get_text(strip=True)
                    socialUrl = artist_social_link.get("href")
                    artist_info[socialType]=socialUrl
            except:
                pass
    except: 
        pass
    finally:
        return artist_info

    

def data_idolrecords(link):

    response = requests.get(link)

    if response.status_code == 200:
        # Get the HTML content
        print("im here")
        html_content = response.content

        # Parse the html content
        soup = BeautifulSoup(html_content, "html.parser")

        artists = []
        # Getting the artist hrefs from the page
        artist_dropdown = soup.find("div", id="artistdropdown")
        artist_links = artist_dropdown.find_all("option")
        
        for artist_link in artist_links[1:]:
            href = artist_link.get("value").split("?")[1]
            artists.append(process_artist(link, href))
        print(artists)
        # Saving the data to a json file
        with open('../NEW_DATA/idolrecords.json', 'w') as f:
            json.dump(artists, f, indent=4, sort_keys=True)
        


def main():
    start_ = time.time()
    data_idolrecords(link)
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
