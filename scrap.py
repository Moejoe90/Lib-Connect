import datetime
import requests
import time
from facebook_scraper import get_posts, exceptions

"""
    here will be the main objects and methods to 
    scrap the facebook pages the idea is init require 
    two arguments the page name and how many page you 
    want to scrape
    
"""

DELAY_SECONDS = 2
TEST_DB = {
    'text': 'Everything you need to know to preorder Hogwarts Legacy, the upcoming open-world RPG set in '
            'the wizarding world of Harry Potter, hundreds of years before the hero arrived.',
    'photo': 'https://assets-prd.ignimgs.com/2022/03/18/hogwarts-legacy-4-1647622573681.jpeg?width=1280',
    'time': datetime.datetime(2022, 3, 24, 16, 31, 9)}


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

    # it's static function now later with database I will make it related to this class
    def where_to_start(self, my_dict):
        test_dict = TEST_DB
        if my_dict['time'] > test_dict['time']:
            return True
        else:
            return False

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
