from database import DataBase
from conftest import scraped_data
from settings import TEST_USER, TEST_URI, TEST_PASSWORD

PAGE_NAME = 'GameSpot'


class TestDataBase:

    def test_connection(self):
        driver = DataBase(uri=TEST_URI, user=TEST_USER, password=TEST_PASSWORD)
        verify = driver.check_connection()
        assert verify is None

    def test_create_nodes(self):
        driver = DataBase(uri=TEST_URI, user=TEST_USER, password=TEST_PASSWORD)
        driver.add_page(PAGE_NAME)
        for post in scraped_data:
            driver.add_post(post_text=post['text'], time=post['time'], image=post['photo'])
            driver.add_relationship(page_name=PAGE_NAME, time=post['time'])
        driver.close()
        assert driver.fine_page(PAGE_NAME)['page_found'] == PAGE_NAME

    # TODO check the last node
    def test_exist_nodes(self):
        pass
