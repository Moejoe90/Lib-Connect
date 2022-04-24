from database import DataBase
from conftest import scraped_data
from settings import TEST_USER, TEST_URI, TEST_PASSWORD
import time

PAGE_NAME = 'GameSpot'


class TestDataBase:

    def test_connection(self):
        driver = DataBase(uri=TEST_URI, user=TEST_USER, password=TEST_PASSWORD)
        verify = driver.check_connection()
        assert verify is None

    # create nodes and destroy it
    def test_create_nodes(self):
        driver = DataBase(uri=TEST_URI, user=TEST_USER, password=TEST_PASSWORD)
        driver.add_page(PAGE_NAME)
        for post in scraped_data:
            driver.add_post(post_text=post['text'], time=post['time'], image=post['photo'])
            driver.add_relationship(page_name=PAGE_NAME, time=post['time'])
        assert driver.find_page(PAGE_NAME)['page_found'] == PAGE_NAME
        time.sleep(4)
        query = (
            "MATCH (n)"
            "DETACH DELETE n"
        )
        # clean database from the nodes we create in testing
        driver.query(query=query)
        driver.close()

    # TODO check the last node
    def test_exist_nodes(self):
        driver = DataBase(uri=TEST_URI, user=TEST_USER, password=TEST_PASSWORD)
        x = driver.find_post(PAGE_NAME)
        for post in scraped_data:
            assert x['time'].time() == post['time'].time()
        print(x['time'], 'its my dict')
        driver.close()
