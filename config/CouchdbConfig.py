from dotenv import load_dotenv
from couchdb2 import Server
import os

# Load environment variables
load_dotenv()


class CouchdbConfig:
    def __init__(self):
        # Fetch CouchDB connection parameters from environment variables
        self.db_uri = os.getenv("COUCHDB_URI")
        self.db_user = os.getenv("COUCHDB_USER")
        self.db_password = os.getenv("COUCHDB_PASSWORD")

        try:
            # Connect to CouchDB server with authentication
            self.server = Server(
                self.db_uri, username=self.db_user, password=self.db_password
            )
            print("CouchDB connection established successfully.")
        except Exception as e:
            self.server = None
            print(f"CouchDB connection failed: {e}")

    def fetch_all_documents(self, db_name):
        """
        Fetch all documents from the specified database.
        """
        if self.server is None:
            print("No connection to the CouchDB server.")
            return

        try:
            # Check if the database exists
            if db_name not in self.server:
                print(f"Database '{db_name}' does not exist.")
                return

            db = self.server[db_name]

            # Fetch and print all documents
            print(f"Fetching documents from '{db_name}'...")
            for document in db:
                print(document)

        except Exception as e:
            print(f"Failed to fetch documents: {e}")

    def create_database(self, db_name):
        """
        Create a new database in CouchDB.
        """
        if self.server is None:
            print("No connection to the CouchDB server.")
            return

        try:
            if db_name in self.server:
                print(f"Database '{db_name}' already exists.")
            else:
                self.server.create(db_name)
                print(f"Database '{db_name}' created successfully.")

        except Exception as e:
            print(f"Failed to create database: {e}")

    def close(self):
        """
        Close the CouchDB connection.
        """
        if self.server is None:
            print("No active CouchDB connection to close.")
        else:
            print("CouchDB connection closed (nothing to explicitly close).")


if __name__ == "__main__":
    config = CouchdbConfig()
    # Test creating a database
    config.create_database("ptrainer_user_routine")
    # Test fetching all documents from a database
    config.fetch_all_documents("ptrainer_user_routine")
    # Close the CouchDB connection
    config.close()
