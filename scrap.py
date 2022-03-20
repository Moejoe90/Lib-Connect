from facebook_scraper import get_posts
import time

"""
    here will be the main objects and methods to scrap the facebook pages
    the idea is init all the required info from the user like 
    (page name, how many post, with comments and reactions or not,
    with videos and photos or not)
"""


class Post(object):

    def __init__(self, page_name: str, num_pages: int):

        self.page_name = page_name
        self.num_pages = num_pages
        self.post_info = {}

    # scrap post text
    def scrap_post_text(self):
        for post in get_posts(self.page_name, pages=self.num_pages):
            time.sleep(2)
            post_text = post['post_text']
            if post_text:
                print(post_text)
            else:
                return 'No text in this post'

    # scrap post image
    def scrap_image(self):
        for post in get_posts(self.page_name, pages=self.num_pages):
            time.sleep(2)
            post_image = post['image']
            if post_image:
                return post_image
            else:
                return 'The post without image'

    # scrap post time
    def scrap_post_date(self):
        for post in get_posts(self.page_name, pages=self.num_pages):
            time.sleep(2)
            date = post['time']
            time_stamp = post['timestamp']
            if date and time_stamp:
                print(date, time_stamp)
            else:
                return None

    # will scrap all the text, photo, and time in dict
    def scrap_full_post(self):
        for post in get_posts(self.page_name, pages=self.num_pages):
            time.sleep(2)
            self.post_info['text'] = post['post_text']
            self.post_info['photo'] = post['image']
            self.post_info['time'] = post['time']
            if self.post_info:
                print(self.post_info)
            else:
                return None
