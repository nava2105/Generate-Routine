from config.PostgresqlConfig import DatabaseConnection
from factories.DatabaseConnectionFactory import DatabaseConnectionFactory  # <-- Correct Import


class PostgresConnectionFactory(DatabaseConnectionFactory):
    """
    Concrete factory for PostgreSQL connections.
    """

    def __init__(self):
        self.db_connection = DatabaseConnection()

    def get_connection(self):
        """
        Return a PostgreSQL database connection.
        """
        return self.db_connection.get_connection()

    def initialize_database(self):
        """
        Ensure schema and required tables exist in PostgreSQL.
        """
        return self.db_connection.initialize_database()
