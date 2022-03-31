from scrap import Post
from conftest import post as test_db
import requests
import datetime


class TestPost:

    def test_connection(self):
        response = requests.get("https://www.facebook.com/")
        assert response.status_code == 200

    def test_resume_scarping(self):
        test = Post('ign', 10)
        test_dict = {'time': datetime.datetime(2022, 3, 29, 16, 31, 9)}
        bool_test = test.resume_scarping(test_dict, test_db)
        print(bool_test)
        assert bool_test

    def test_scraping(self):
        test = Post('ign', 10)
        posts = test.scrape_full_post()
        assert posts
