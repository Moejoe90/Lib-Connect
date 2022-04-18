from settings import NEO4J_USER, NEO4J_URI, NEO4J_PASSWORD
from neo4j import GraphDatabase, exceptions
from neo4j.exceptions import ServiceUnavailable
import logging


class DataBase:

    def __init__(self):
        self.driver = None
        try:
            self.driver = GraphDatabase.driver(uri=NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        except Exception(exceptions.AuthError):
            raise

    def close(self):
        if self.driver is not None:
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

    def add_post(self, post_text, image):
        with self.driver.session() as session:
            try:
                session.write_transaction(self.create_post_node, post_text, image)
                print(f"the post node has been created")
            except Exception(exceptions.SessionExpired):
                raise

    def add_relationship(self, page_name, post, time):
        with self.driver.session() as session:
            try:
                session.write_transaction(self.create_relationship, page_name, post, time)
                print(f"{page_name}--[{time}]-->{post}")
            except Exception(exceptions.SessionExpired):
                raise

    @staticmethod
    def create_page_node(tx, name):
        try:
            return tx.run("CREATE (a:Page {Name: $name})", name=name)
        except Exception(exceptions.CypherSyntaxError):
            raise

    @staticmethod
    def create_post_node(tx, post_text, image):
        query = (
            "CREATE (b:Post {Name: 'Post', Text: $text, Photo: $image})"
            "RETURN b"
        )
        result = tx.run(query, text=post_text, image=image)
        try:
            return [{
                "b": row["b"]["Post", "Text", "Photo"]
            } for row in result]

        except ServiceUnavailable as exception:
            logging.error(f"{query} raised an error: \n {exception}")
            raise

    @staticmethod
    def create_relationship(tx, page_name, post, time):
        query = (
            "MATCH (a: Page), (b: Post)"
            "WHERE a.Name = $name"
            "CREATE (a)-[t:Date {Time:$time}]->(b)"
            "RETURN t;"
        )
        result = tx.run(query, name=page_name, post=post, time=time)
        try:
            return result
        except ServiceUnavailable as exception:
            logging.error(f"{query} raised an error: \n {exception}")
            raise


