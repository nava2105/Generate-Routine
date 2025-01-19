from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()


class Neo4jConfig:
    def __init__(self):
        db_uri = os.getenv('NEO4J_URI')
        db_user = os.getenv('NEO4J_USER')
        db_password = os.getenv('NEO4J_PASSWORD')

        self.driver = GraphDatabase.driver(db_uri, auth=(db_user, db_password))

    def fetch_all_nodes(self):
        with self.driver.session() as session:
            result = session.run("MATCH (n) RETURN n")
            for record in result:
                print(record)

    def close(self):
        self.driver.close()


if __name__ == "__main__":
    config = Neo4jConfig()
    config.fetch_all_nodes()
    config.close()
