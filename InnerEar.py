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

link = config.get("Inner Ear", "link")

# def process_artist(link, artist_name):
#     artist_url = link
#     artist_response = requests.get(artist_url)
#     # If the correct url is hit
#     artist_info = {}
#     try:
#         if artist_response.status_code == 200:
#             artist_html_content = artist_response.content
#             artist_soup = BeautifulSoup(artist_html_content, "html.parser")
#             try:
#                 artist_social_links = artist_soup.find('ul', class_="vcmp-socials").find_all("li")
#                 artist_info["ArtistName"] = artist_name
#                 for artist_social_link in artist_social_links:
#                     socialUrl = artist_social_link.find("a").get("href")
#                     if ("facebook" in socialUrl):
#                         artist_info["Facebook"]=socialUrl
#                     elif ("twitter" in socialUrl):
#                         artist_info["Twitter"]=socialUrl
#                     elif ("instagram" in socialUrl):
#                         artist_info["Instagram"]=socialUrl
#                     elif ("youtube" in socialUrl):
#                         artist_info["Youtube"]=socialUrl
#                     elif ("spotify" in socialUrl):
#                         artist_info["Spotify"]=socialUrl
#                     elif ("soundcloud" in socialUrl) or ("SoundCloud" in socialUrl):
#                         artist_info["SoundCloud"]=socialUrl
#                     elif ("itunes" in socialUrl):
#                         artist_info["ITunes"]=socialUrl
#                     elif ("apple" in socialUrl):
#                         artist_info["Apple Music"]=socialUrl
#                     else:
#                         artist_info["Social Media Link"]=socialUrl
#             except:
#                 pass
#     except: 
#         pass
#     finally:
#         return artist_info

    

def data_InnerEar(link):

    response = requests.get(link)
    print(response.status_code)
    if response.status_code == 200:
        # Get the HTML content
        html_content = response.content

        # Parse the html content
        soup = BeautifulSoup(html_content, "html.parser")
        

        artists = []
        # Getting the artist hrefs from the page
        artist_content = soup.find("body", id="bg")
        art = artist_content.find("div", class_="container")
        # artist_links = artist_content.find_all("div", class_="isVueArticle outerol")
        print(art)

        # for artist_link in artist_links:
        #     href = artist_link.get("href")
        #     artist_name = artist_link.find("h3").get_text(strip=True)
        #     artists.append(process_artist(href, artist_name))
        # # Saving the data to a json file
        # with open('../NEW_DATA/ActiveTalentAgency.json', 'w') as f:
        #     json.dump(artists, f, indent=4, sort_keys=True)
        


def main():
    start_ = time.time()
    data_InnerEar(link)
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
