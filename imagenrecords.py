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

link = config.get("imagenrecords", "link")


# Function to process the artist hrefs
def process_artist(href):
    artist_url = href
    artist_response = requests.get(artist_url)
    # If the correct url is hit
    artist_info = {}
    try:
        if artist_response.status_code == 200:
            artist_html_content = artist_response.content
            artist_soup = BeautifulSoup(artist_html_content, "html.parser")
            try:
                artist_name = artist_soup.find('div', class_='artist_desc sr_it-meta').find('h1')
                artist_info = {"ArtistName": artist_name.text}

                artist_social_links = artist_soup.find_all("div", class_="social_icon")
                
                for artist_social_link in artist_social_links:
                    socialType = artist_social_link.find('a').get_text(strip=True)
                    socialUrl = artist_social_link.find('a').get("href")
                    
                    artist_info[socialType]=socialUrl
            except:
                pass
    except: 
        pass
    finally:
        return artist_info
    

def data_imagenrecords(link):

    response = requests.get(link)
    print(response.status_code)
    
    
    if response.status_code == 200:
        # Get the HTML content
        print("Im here")
        html_content = response.content


        # Parse the html content
        soup = BeautifulSoup(html_content, "html.parser")
        print(soup) 

        # Getting the artist hrefs from the page
        artist_dropdown = soup.find("ul", class_="sub-menu")
        print(artist_dropdown)
        artist_links = artist_dropdown.find_all("li")
        print(artist_links) 

        # artists = []
        # # Processing the href links for each artist to return their social media links
        # for artist_link in artist_links:
        #     href = artist_link.get("href")
        #     artists.append(process_artist(href))
        
        
        # Saving the data to a json file
        # c

def main():
    start_ = time.time()
    data_imagenrecords(link)
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

        


    
    

