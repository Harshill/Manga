import os
import shutil
import requests
import matplotlib.pyplot as graph
from tqdm import tqdm, trange
from time import sleep
from selenium import webdriver

driver = webdriver.Chrome()

chapter, page = 1, 1

for curr_chapter in trange(chapter, 921):
    driver.get(f'https://www.mangareader.net/one-piece/{curr_chapter}')

    # Make folder
    folder = f'Data/Onepiece/chapter_{curr_chapter}'
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder)

    # Get images
    while chapter == curr_chapter:
        # Get image
        image = driver.find_element_by_id('img')
        source = image.get_attribute('src')
        chapter = int(source.split('/one-piece', maxsplit=2)[1][1:])

        if chapter != curr_chapter:
            break

        # Save image
        response = requests.get(source, stream=True)
        with open(f'{folder}/onepiece_chapter_{chapter}_page_{page}.jpg', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response

        # Next image
        image.click()
        page += 1
        sleep(0.25)

    # Reset page number
    page = 1
