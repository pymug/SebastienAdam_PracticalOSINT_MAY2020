#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The purpose of this script is to show how to automatically download images from a web site.

As an example, we will use the Pepper&Carrot site, a free (libre) and open-source webcomic.

(c) Sébastien Adam 2020
    Website: https://www.sebastienadam.be
    diaspora*: https://diasp.de/u/sebastienadam
    LinkedIn: https://www.linkedin.com/in/sebastien-adam-be/
"""

from bs4 import BeautifulSoup
from io import BytesIO
from pathlib import Path
from PIL import Image

import requests

main_url = 'https://www.peppercarrot.com/'

r_main = requests.get(main_url)
if r_main.status_code != 200:
    print(f'Failed to load {main_url}: {r_main.status_code}')
    quit()

soup_main = BeautifulSoup(r_main.text, 'html5lib')
soup_homecontent = soup_main.find('div', class_='homecontent')
for figure in soup_homecontent.find_all('figure'):
    episode_link = figure.find('a')
    print(f"{episode_link['title']} : {episode_link['href']}")
    r_episode = requests.get(episode_link['href'])
    if r_episode.status_code != 200:
        print(f'Failed to load {main_url}: {r_main.status_code}')
        continue
    soup_episode = BeautifulSoup(r_episode.text, 'html5lib')
    for image in soup_episode.find_all('img', class_='comicpage'):
        img_url = image['src']
        print(img_url)
        r_image = requests.get(img_url)
        if r_image.status_code != 200:
            print(f'Failed to load {img_url}: {r_image.status_code}')
            continue
        i = Image.open(BytesIO(r_image.content))
        image_name = Path(img_url).name
        i.save(image_name)

