from settings import NEO4J_USER, NEO4J_URI, NEO4J_PASSWORD
from neo4j import GraphDatabase, exceptions


class DataBase:

    def __init__(self):
        self.driver = GraphDatabase.driver(uri=NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    def close(self):
        self.driver.close()

    def check_connection(self):
        self.driver.verify_connectivity()

    def add_page(self, name):
        with self.driver.session() as session:
            try:
                session.write_transaction(self.create_page_node, name)
                print(f"the first node named {name} has been created")
            except Exception(exceptions.SessionExpired):
                raise

    def add_post(self, post_text):
        with self.driver.session() as session:
            try:
                session.write_transaction(self.create_post_node, post_text)
                print(f"the post node has been created")
            except Exception(exceptions.SessionExpired):
                raise

    @staticmethod
    def create_page_node(tx, name):
        try:
            return tx.run("CREATE (a:Page {name: $name})", name=name)
        except Exception(exceptions.CypherSyntaxError):
            raise

    @staticmethod
    def create_post_node(tx, post_text):
        try:
            return tx.run("CREATE (b:Post {Name: 'Post', Text: $text})", text=post_text)
        except Exception(exceptions.CypherSyntaxError):
            raise



