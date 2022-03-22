from scrap import Post, check_connection
from facebook_scraper import exceptions

facebook = Post('ign', 2)


check_connection('https://www.facebook.com')


# I want to learn more about error handling with scrapping
# and where I should use them here or in scrap.py
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
