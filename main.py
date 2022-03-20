from scrap import Post
from facebook_scraper import exceptions

facebook = Post('ign', 10)


# I want to learn more about error handling with scrapping
# and where I should use them here or in scrap.py
def grab_facebook():
    try:
        facebook.scrap_full_post()
    except exceptions.NotFound:
        print("Post, page or profile not found / doesn't exist / deleted")
    finally:
        print('its done')


if __name__ == '__main__':
    grab_facebook()
