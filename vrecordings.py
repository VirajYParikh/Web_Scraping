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

link = config.get("vrecordings", "link")



# Function to process the artist hrefs
def process_artist(href):
    artist_url = "https://vrecordings.com" + href
    artist_response = requests.get(artist_url)
    # If the correct url is hit
    if artist_response.status_code == 200:
        artist_html_content = artist_response.content
        artist_soup = BeautifulSoup(artist_html_content, "html.parser")
        artist_name = artist_soup.find("h2",class_="page-heading")
        print(artist_name.text)
        artist_social_links = artist_soup.find("div", id="social-btn-group").find_all("a")
        artist_info = {"ArtistName": artist_name.text}
        for artist_social_link in artist_social_links:
            socialType = artist_social_link.get("title")
            socialUrl = artist_social_link.get("href")
            artist_info[socialType]=socialUrl
        return artist_info
            
        

def data_vrecordings(link):

    response = requests.get(link)
    
    if response.status_code == 200:
        # Get the HTML content
        html_content = response.content

        # Parse the html content
        soup = BeautifulSoup(html_content, "html.parser")

        # Getting the artist hrefs from the page
        artist_links = soup.find_all("a", class_="overlay-link");
        artists = []
        # Processing the href links for each artist to return their social media links
        for artist_link in artist_links:
            href = artist_link.get("href")
            artists.append(process_artist(href))
        print(artists)

        with open('../NEW_DATA/vrecordings.json', 'w') as f:
            json.dump(artists, f, indent=4, sort_keys=True)

def main():
    start_ = time.time()
    data_vrecordings(link)
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

        


    
    

