from database import DataBase
from scrap import Post
from settings import TEST_USER, TEST_URI, TEST_PASSWORD


PAGE_NAME = 'GameSpot'


class TestDataBase:

    def __int__(self):
        self.data = DataBase(uri=TEST_URI, user=TEST_USER, password=TEST_PASSWORD)
        self.facebook = Post(page_name=PAGE_NAME, num_pages=10)

    def test_connection(self):
        driver = DataBase(uri=TEST_URI, user=TEST_USER, password=TEST_PASSWORD)
        verify = driver.check_connection()
        assert verify is None

    # TODO
    def test_create_nodes(self):
        driver = DataBase(uri=TEST_URI, user=TEST_USER, password=TEST_PASSWORD)
        driver.add_page(PAGE_NAME)
        for post in self.facebook.scrape_full_post():
            driver.add_post(post_text=post['text'], time=post['time'], image=post['photo'])
            driver.add_relationship(page_name=PAGE_NAME, time=post['time'])

    # TODO
    def test_exist_nodes(self):
        pass
