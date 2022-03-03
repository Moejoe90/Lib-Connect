from facebook_scraper import get_posts

"""
    here will be the main objects and methods to scrap the facebook pages
    the idea is init all the required info from the user like 
    (page name, how many post, with comments and reactions or not,
    with videos and photos or not)
"""


class Post(object):

    def __init__(self, page_name, num_pages):
        self.page_name = page_name
        self.num_pages = num_pages

    def scrap_post_text(self):
        for post in get_posts(self.page_name, pages=self.num_pages):
            post_text = post['post_text']
            if post_text:
                return post_text
            else:
                return 'No text in this post'

    def scrap_image(self):
        for post in get_posts(self.page_name, pages=self.num_pages):
            post_image = post['image']
            if post_image:
                return post_image
            else:
                return 'The post without image'

    def scrap_video(self):
        for post in get_posts(self.page_name, pages=self.num_pages, youtube_dl=False):
            post_video = post['video']
            if post_video:
                print(post_video)


# testing
face = Post('ign', num_pages=3)
#face.scrap_post_text()
face.scrap_image()
# face.scrap_video()
