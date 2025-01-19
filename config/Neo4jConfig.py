from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()


class Neo4jConfig:
    """
    Configuration for Neo4j database connections.
    """

    def __init__(self):
        self.db_uri = os.getenv('NEO4J_URI')
        self.db_user = os.getenv('NEO4J_USER')
        self.db_password = os.getenv('NEO4J_PASSWORD')
        self.driver = GraphDatabase.driver(self.db_uri, auth=(self.db_user, self.db_password))

    def get_driver(self):
        """
        Returns the Neo4j driver instance.
        """
        return self.driver

    def close(self):
        """
        Closes the connection to the Neo4j database.
        """
        self.driver.close()
