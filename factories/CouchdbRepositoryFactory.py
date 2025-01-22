from factories.RepositoryFactory import RepositoryFactory
from config.CouchdbConfig import CouchdbConfig
from repositories.RoutinesRepository import RoutinesRepository


class CouchdbRepositoryFactory(RepositoryFactory):
    """
    Factory to create CouchDB-specific repositories.
    """

    def __init__(self):
        """
        Initializes the repository factory with a CouchDB configuration.
        """
        self.config = CouchdbConfig()

    def create_routines_repository(self):
        """
        Creates and returns a RoutinesRepository for CouchDB.

        :return: A RoutinesRepository instance.
        """
        return RoutinesRepository(self.config.server)

    def create_volumes_repository(self):
        """
        Placeholder method: Volumes repository is not relevant for CouchDB.
        Raises an error if called.
        """
        raise NotImplementedError("CouchDB does not support a volumes repository.")

    def close(self):
        """
        Closes the CouchDB connection when the factory is destroyed.
        """
        self.config.close()
