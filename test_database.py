from database import DataBase


class TestDataBase:

    def test_connection(self):
        drive = DataBase()
        verify = drive.check_connection()
        assert verify is None

    # TODO
    def test_create_nodes(self):
        pass

    # TODO
    def test_exist_nodes(self):
        pass
