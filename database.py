from settings import NEO4J_USER, NEO4J_URI, NEO4J_PASSWORD
from py2neo import Node, Graph, Relationship, Subgraph


class DataBase:

    def __init__(self):
        self.driver = Graph(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    def close(self):
        pass

    def create_nodes(self, page, post, time):

        properties = {"time": f"{time}"}
        page_node = Node("Page", name=f"{page}")
        post_node = Node("Post", text=f"{post}")
        relationship = Relationship(page_node, "Date", post_node, **properties)
        nodes = [page_node, post_node]
        subgraph = Subgraph(nodes, relationship)
        tx = self.driver.begin()
        tx.create(subgraph)
        self.driver.commit(tx)



