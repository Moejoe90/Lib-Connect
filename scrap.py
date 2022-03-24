from facebook_scraper import get_posts, exceptions
import requests
import time

"""
    here will be the main objects and methods to 
    scrap the facebook pages the idea is init require 
    two arguments the page name and how many page you 
    want to scrape
    
"""

DELAY_SECONDS = 2


class Post(object):

    def __init__(self, page_name: str, num_pages: int):

        self.page_name = page_name
        self.num_pages = num_pages
        self.post_info = {}
        self.url = "https://www.facebook.com/"

    def check_connection(self):
        try:
            get = requests.get(self.url)
            if get.status_code == 200:
                print(f"{self.url}: is reachable")
            else:
                print(f"{self.url}: is Not reachable, status_code: {get.status_code}")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"{self.url}: is Not reachable \nErr: {e}")

    # will scrap all the text, photo, and time in dict
    def scrape_full_post(self):
        keys = ['text', 'photo', 'time']

        for post in get_posts(self.page_name, pages=self.num_pages):
            time.sleep(DELAY_SECONDS)
            values = [post['post_text'], post['image'], post['time']]
            self.post_info = dict(zip(keys, values))
            if self.post_info:
                yield self.post_info
            else:
                raise Exception(exceptions.NotFound)
