from scrap import Post
from facebook_scraper import exceptions

facebook = Post('ign', 2)


def grab_facebook():
    try:
        for i, j in enumerate(facebook.scrape_full_post()):
            if facebook.where_to_start(j):
                print(f"{i} - {j}")
            else:
                print("post scraped before")
                break
    except exceptions.NotFound:
        print("Post, page or profile not found / doesn't exist / deleted")
    finally:
        print('its done')


if __name__ == '__main__':
    grab_facebook()
