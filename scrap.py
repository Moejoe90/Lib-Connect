import requests
import time
from facebook_scraper import get_posts, exceptions
from conftest import post as test_db


DELAY_SECONDS = 2


class Post(object):

    def __init__(self, page_name: str, num_pages: int):

        self.page_name = page_name
        self.num_pages = num_pages
        self.post_info = {}
        self.url = "https://www.facebook.com/"

    def check_connection(self) -> bool:
        try:
            get = requests.get(self.url)
            if get.status_code == 200:
                print(f"{self.url}: is reachable")
                return True
            else:
                time.sleep(1)
                print(f"{self.url}: is Not reachable, status_code: {get.status_code}")
                return False
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(f"{self.url}: is Not reachable \nErr: {e}")

    # will scrap all the text, photo, and time as one dict
    def scrape_full_post(self) -> dict:
        if self.check_connection():
            keys = ['text', 'photo', 'time']
            try:
                for post in get_posts(self.page_name, pages=self.num_pages):
                    if self.resume_scarping(f_posts=post, last_post=test_db):
                        print("resuming scraping..")
                        time.sleep(DELAY_SECONDS)
                        values = [post['post_text'], post['image'], post['time']]
                        self.post_info = dict(zip(keys, values))
                        if self.post_info:
                            yield self.post_info
                        else:
                            raise Exception(exceptions.NotFound)
                    else:
                        print("Last post already scraped")
            except exceptions.NotFound as e:
                raise print(e)

    @staticmethod
    def resume_scarping(f_posts: dict, last_post: dict) -> bool:

        if f_posts['time'] > last_post['time']:
            return True
        else:
            return False
