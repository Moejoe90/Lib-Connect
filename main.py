from scrap import Post
from conftest import post as db

facebook = Post('ign', 10)


def grab_facebook():
    for i, j in enumerate(facebook.scrape_full_post()):
        if facebook.resume_scarping(j, db):
            print(f"{i} - {j}")


if __name__ == '__main__':
    grab_facebook()
