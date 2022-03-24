from scrap import Post
from facebook_scraper import exceptions

facebook = Post('ign', 2)


def grab_facebook():
    try:
        for i, j in enumerate(facebook.scrape_full_post()):
            print(f"{i} - {j}")
    except exceptions.NotFound:
        print("Post, page or profile not found / doesn't exist / deleted")
    finally:
        print('its done')


if __name__ == '__main__':
    grab_facebook()
