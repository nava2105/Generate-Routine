import os
import psycopg2
from psycopg2 import Error
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()


class DatabaseConnection:
    """
    A class responsible for establishing and managing PostgreSQL connections.
    """

    def __init__(self):
        # PostgreSQL connection parameters
        self.conn_params = {
            "dbname": os.getenv('POSTGRESQL_DBNAME'),
            "user": os.getenv('POSTGRESQL_USER'),
            "password": os.getenv('POSTGRESQL_PASSWORD'),
            "host": os.getenv('POSTGRESQL_HOST'),
            "port": os.getenv('POSTGRESQL_PORT')
        }

    def get_connection(self):
        """
        Establish and return a connection to the PostgreSQL database.
        """
        try:
            connection = psycopg2.connect(**self.conn_params)
            print("PostgreSQL connection established successfully.")
            return connection
        except Error as e:
            print(f"Error connecting to PostgreSQL: {e}")
            raise

    def initialize_database(self):
        """
        Checks if the required schema and table exist in the database.
        Otherwise, it runs the PostgreSQL initialization script.
        """
        creation_sql = "PostgreSQLCreation.sql"
        try:
            connection = self.get_connection()
            with connection.cursor() as cursor:
                # Check if the schema exists
                cursor.execute("""
                    SELECT schema_name 
                    FROM information_schema.schemata 
                    WHERE schema_name = 'ptrainer_volumes';
                """)
                schema_exists = cursor.fetchone()

                if not schema_exists:
                    print("Schema does not exist, initializing database...")
                    # Execute the SQL script
                    with open(creation_sql, 'r') as file:
                        cursor.execute(file.read())
                    connection.commit()
                    print("Database initialized successfully.")
                else:
                    print("Schema already exists.")

        except Exception as e:
            print(f"Error during database initialization: {e}")
        finally:
            if connection:
                connection.close()
