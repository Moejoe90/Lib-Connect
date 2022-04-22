from neo4j import GraphDatabase, exceptions, basic_auth
from neo4j.exceptions import ServiceUnavailable
from abc import ABC, abstractmethod
import logging


class Nodes(ABC):

    @abstractmethod
    def create_page_node(self, tx, name):
        pass

    @abstractmethod
    def create_relationship(self, tx, page_name, time):
        pass

    @abstractmethod
    def create_post(self, tx, post_text, image, time):
        pass


class DataBase(Nodes):

    def __init__(self, uri, user, password):
        self.uri = uri
        self.user = user
        self.password = password
        self.driver = None
        try:
            self.driver = GraphDatabase.driver(uri, auth=basic_auth(user, password))
        except Exception(exceptions.AuthError):
            raise

    def close(self):
        if self.driver is not None:
            self.driver.close()
        else:
            raise exceptions.DriverError

    def check_connection(self):
        self.driver.verify_connectivity()

    def create_page_node(self, tx, name):
        try:
            return tx.run("CREATE (a:Page {Name: $name})", name=name)
        except Exception(exceptions.CypherSyntaxError):
            raise

    def create_relationship(self, tx, page_name, time):
        query = (
            "MATCH (a: Page), (b: Post) "
            "WHERE a.Name = $name AND b.Time = $time "
            "CREATE (a)-[t:Date {Time:$time}]->(b) "
            "RETURN t"
        )
        result = tx.run(query, name=page_name, time=time)
        try:
            return result
        except ServiceUnavailable as exception:
            logging.error(f"{query} raised an error: \n {exception}")
            raise

    def create_post(self, tx, post_text, image, time):
        query = (
            ""
            "CREATE (b:Post {Name: 'Post', Text: $text, Photo: $image, Time: $time}) "
            "RETURN b"
        )
        result = tx.run(query, text=post_text, image=image, time=time)
        try:
            return result
        except ServiceUnavailable as exception:
            logging.error(f"{query} raised an error: \n {exception}")
            raise

    def add_page(self, name):
        with self.driver.session() as session:
            try:
                session.write_transaction(self.create_page_node, name)
                print(f"the page node named {name} has been created")
            except Exception(exceptions.SessionExpired):
                raise

    def add_post(self, post_text, image, time):
        with self.driver.session() as session:
            try:
                session.write_transaction(self.create_post, post_text, image, time)
                print(f"the post node has been created")
            except Exception(exceptions.SessionExpired):
                raise

    def add_relationship(self, page_name, time):
        with self.driver.session() as session:
            try:
                session.write_transaction(self.create_relationship, page_name, time)
                print(f"{page_name}--[{time}]-->'post'")
            except Exception(exceptions.SessionExpired):
                raise
