from neo4j import GraphDatabase, exceptions, basic_auth
from neo4j.exceptions import ServiceUnavailable
from abc import ABC, abstractmethod
from exceptions import PageNotFound
import logging
import datetime

date = datetime.datetime.now()
ts = date.timestamp()


class Nodes(ABC):

    @abstractmethod
    def _create_page_node(self, tx, name):
        pass

    @abstractmethod
    def _create_relationship(self, tx, page_name, time):
        pass

    @abstractmethod
    def _create_post(self, tx, post_text, image, time):
        pass

    @abstractmethod
    def _find_page(self, tx, page_name):
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

    def _create_page_node(self, tx, name):
        try:
            return tx.run("CREATE (a:Page {Name: $name, Created_at: $timestamp})", name=name, timestamp=ts)
        except Exception(exceptions.CypherSyntaxError):
            raise

    def _create_relationship(self, tx, page_name, time):
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

    def _create_post(self, tx, post_text, image, time):
        query = (
            ""
            "CREATE (b:Post {Name: 'Post', Text: $text, Photo: $image, Time: $time, Created_at:$timestamp}) "
            "RETURN b"
        )
        result = tx.run(query, text=post_text, image=image, time=time, timestamp=ts)
        try:
            return result
        except ServiceUnavailable as exception:
            logging.error(f"{query} raised an error: \n {exception}")
            raise

    def _find_page(self, tx, page_name):
        query = (
            "MATCH (a:Page) "
            "WHERE a.Name = $page_name "
            "RETURN a.Name AS name"
        )

        result = tx.run(query, page_name=page_name)
        return [row['name'] for row in result]

    def add_page(self, name):
        with self.driver.session() as session:
            try:
                session.write_transaction(self._create_page_node, name)
                print(f"the page node named {name} has been created")
            except Exception(exceptions.SessionExpired):
                raise

    def add_post(self, post_text, image, time):
        with self.driver.session() as session:
            try:
                session.write_transaction(self._create_post, post_text, image, time)
                print(f"the post node has been created")
            except Exception(exceptions.SessionExpired):
                raise

    def add_relationship(self, page_name, time):
        with self.driver.session() as session:
            try:
                session.write_transaction(self._create_relationship, page_name, time)
                print(f"{page_name}--[{time}]-->'post'")
            except Exception(exceptions.SessionExpired):
                raise

    def fine_page(self, page_name):
        with self.driver.session() as session:
            try:
                result = session.read_transaction(self._find_page, page_name)
                return {'page_found': row for row in result}
            except PageNotFound:
                print(f"{page_name} Page not found in database")

    def query(self, query, parameters=None, db=None):
        assert self.driver is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            session = self.driver.session(database=db) if db is not None else self.driver.session()
            response = list(session.run(query, parameters))
        except Exception as e:
            print("Query failed:", e)
        finally:
            if session is not None:
                session.close()
        return response
