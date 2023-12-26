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

link = config.get("ignitionrecords", "link")

import selenium
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


# def process_artist(href):
#     artist_url = link + "artists/index.php?" + href
#     artist_response = requests.get(artist_url)
#     # If the correct url is hit
#     artist_info = {}
#     try:
#         if artist_response.status_code == 200:
#             artist_html_content = artist_response.content
#             artist_soup = BeautifulSoup(artist_html_content, "html.parser")
#             try:
#                 artist_name = artist_soup.find('span', class_='headlinetitle').get_text(strip=True)
#                 artist_info = {"ArtistName": artist_name}

#                 artist_links_location = artist_soup.find("div", id="footer-center")
#                 artist_social_links = artist_links_location.find_all("a", class_="nav-footer")

#                 for artist_social_link in artist_social_links:
#                     socialType = artist_social_link.get_text(strip=True)
#                     socialUrl = artist_social_link.get("href")
#                     artist_info[socialType]=socialUrl
#             except:
#                 pass
#     except: 
#         pass
#     finally:
#         return artist_info

    

def data_ignitionrecords(link):


    s=Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)
    driver.maximize_window()
    driver.get(link)
    elements = driver.find_elements(By.Class, '//*[@id="userActivityGraph"]')

    response = requests.get(link)

    if response.status_code == 200:
        # Get the HTML content
        html_content = response.content

        # Parse the html content
        soup = BeautifulSoup(html_content, "html.parser")

        # Getting the artist hrefs from the page
        artists_info = soup.find_all("div", class_="artist-info")
        artists = []
        for artist_info in artists_info:
            artist_name = artist_info.find("h3", class_="artist-title").get_text(strip=True)
            artist = {"ArtistName":artist_name}
            artist_social_links = artist_info.find("div", class_="socials").find_all("a")
            print(artist_social_links)
            for artist_social_link in artist_social_links:
                socialType_soup = artist_social_link.find("svg")
                print(socialType_soup['data-icon'])
                # socialType = socialType_soup.get("data-icon")
                socialUrl = artist_social_link.get("href")
                # artist[socialType]=socialUrl    
            artists.append(artist)
        print(artists)



        # artist_links = artist_dropdown.find_all("option")
        
        # for artist_link in artist_links[1:]:
        #     href = artist_link.get("value").split("?")[1]
        #     artists.append(process_artist(link, href))

        # # Saving the data to a json file
        # with open('../NEW_DATA/idolrecords.json', 'w') as f:
        #     json.dump(artists, f, indent=4, sort_keys=True)
        


def main():
    start_ = time.time()
    data_ignitionrecords(link)
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
