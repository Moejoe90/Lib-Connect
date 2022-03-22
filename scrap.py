from facebook_scraper import get_posts
import requests
import time

"""
    here will be the main objects and methods to 
    scrap the facebook pages the idea is init require 
    two arguments the page name and how many page you 
    want to scrape
    
"""


def check_connection(url):
    try:
        # Get Url
        get = requests.get(url)
        # if the request succeeds
        if get.status_code == 200:
            print(f"{url}: is reachable")
        else:
            print(f"{url}: is Not reachable, status_code: {get.status_code}")

    # Exception
    except requests.exceptions.RequestException as e:
        # print URL with Errs
        raise SystemExit(f"{url}: is Not reachable \nErr: {e}")


class Post(object):

    def __init__(self, page_name: str, num_pages: int):

        self.page_name = page_name
        self.num_pages = num_pages
        self.post_info = {}

    # will scrap all the text, photo, and time in dict
    def scrape_full_post(self):
        keys = ['text', 'photo', 'time']

        for post in get_posts(self.page_name, pages=self.num_pages):
            time.sleep(2)
            values = [post['post_text'], post['image'], post['time']]
            self.post_info = dict(zip(keys, values))
            if self.post_info:
                yield self.post_info
            else:
                raise Exception("Scraping failure, check your internet connection")
