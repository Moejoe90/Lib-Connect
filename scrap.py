from facebook_scraper import get_posts

"""
    here will be the main objects and methods to scrap the facebook pages
    the idea is init all the required info from the user like 
    (page name, how many post, with comments and reactions or not,
    with videos and photos or not)
"""


class Post(object):

    def __init__(self, page_name):
        self.page_name = page_name

    def scrap(self):
        for post in get_posts(self.page_name, pages=1):
            print(post['text'][:50])

    def scrap_photo(self):
        pass


# testing
face = Post('ign')
face.scrap()
