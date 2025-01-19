from abc import ABC, abstractmethod


class DatabaseConnectionFactory(ABC):
    """
    Abstract factory for creating database connections.
    """

    @abstractmethod
    def get_connection(self):
        """
        Create and return the appropriate database connection.
        """
        pass

    @abstractmethod
    def initialize_database(self):
        """
        Initialize database schema if not already present (optional).
        """
        pass