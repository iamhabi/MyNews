from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

import json
import time
import threading
import requests
import datetime
import os

custom_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"

service = Service()

options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={custom_user_agent}")
options.add_argument('--headless')
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920,1080")
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')


SERVER_PORT = os.environ['SERVER_PORT']
news_url = f'http://localhost:{SERVER_PORT}/api/news/'


def scraping():
    scraping_thread = threading.Thread(target=scraping_loop)
    scraping_thread.start()


def scraping_loop():
    while True:
        print(datetime.datetime.now())

        scraping_internal()

        time.sleep(60 * 60)


def scraping_internal():
    try:
        with open("news-infos.json") as file:
            news_infos = json.load(file)

            for news_info in news_infos:
                url = news_info["url"]
                base_xpath = news_info["base_xpath"]
                title_xpath = news_info["title_xpath"]

                driver = webdriver.Chrome(service=service, options=options)
                driver.get(url)

                elements = driver.find_elements(By.XPATH, base_xpath)
                titles = driver.find_elements(By.XPATH, base_xpath + title_xpath)

                if len(elements) != len(titles):
                    print("Something wrong while scraping: " + url)

                for (title, element) in zip(titles, elements):
                    url = element.find_element(By.TAG_NAME, "a").get_attribute("href")

                    if (title.text == ""):
                        title = title.get_attribute("innerHTML")
                    else:
                        title = title.text

                    data = {
                        "title": title,
                        "url": url
                    }

                    requests.post(url=news_url, data=data)

                driver.quit()

    except Exception as e:
        print("Error", e)

    driver.quit()