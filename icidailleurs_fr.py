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

link = config.get("icidailleurs_fr", "link")


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
    

def data_icidailleurs(link):

    response = requests.get(link)
    
    if response.status_code == 200:
        # Get the HTML content
        html_content = response.content

        # Parse the html content
        soup = BeautifulSoup(html_content, "html.parser")

        # Getting the artist hrefs from the page
        artist_links = soup.find_all("a", class_="elementor-post__thumbnail__link")
        artists = []
        
        # Processing the href links for each artist to return their social media links
        for artist_link in artist_links:
            href = artist_link.get("href")
            artists.append(process_artist(href))
        
        # Getting the page number links
        page_number_links = soup.find_all("a", class_="page-numbers")
        
        # Getting the last page number
        page_number = []
        for page_number_link in page_number_links:
            text = ''.join(page_number_link.find_all(text=True, recursive=False)).strip()
            page_number.append(text)

        
        # Getting the artist hrefs from the all artist pages
        for i in page_number:
            next_page_link = link + i + "/"
            print(next_page_link)
            response = requests.get(next_page_link)
            if response.status_code == 200:
                html_content = response.content
                soup = BeautifulSoup(html_content, "html.parser")
                
                artist_links = soup.find_all("a", class_="elementor-post__thumbnail__link")
                for artist_link in artist_links:
                    href = artist_link.get("href")
                    artists.append(process_artist(href))

        # Saving the data to a json file
        with open('../NEW_DATA/icidailleurs_fr.json', 'w') as f:
            json.dump(artists, f, indent=4, sort_keys=True)

def main():
    start_ = time.time()
    data_icidailleurs(link)
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

        


    
    

