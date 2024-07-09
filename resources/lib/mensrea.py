import requests
import re
from bs4 import BeautifulSoup

def get_soup1(url1):
    page = requests.get(url1)
    soup1 = BeautifulSoup(page.text, 'html.parser')
    print("type: ", type(soup1))
    return soup1

def get_playable_mensrea(soup):
    subjects = []
    for content in soup.find_all('item'):
        try:
            link = content.find('enclosure').get('url')
            title = content.find('title').get_text()
            thumbnail = content.find('itunes:image').get('href')
            desc = content.find('itunes:subtitle').get_text()  # Extract the subtitle
        except AttributeError:
            continue
        
        item = {
            'url': link,
            'title': title,
            'thumbnail': thumbnail,
            'description': desc,
        }
        subjects.append(item)
    
    return subjects

def compile_playable_mensrea(playable_deconstructed):
    items = []
    for podcast in playable_mensrea:
        items.append({
            'label': podcast['title'],
            'thumbnail': podcast['thumbnail'],
            'path': podcast['url'],
            'is_playable': True,
            'info': {
                'plot': podcast.get('description', ''),
            }
        })
    return items