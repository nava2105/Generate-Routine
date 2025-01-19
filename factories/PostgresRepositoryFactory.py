from repositories.VolumesRepository import VolumesRepository
from factories.PostgresConnectionFactory import PostgresConnectionFactory
from factories.RepositoryFactory import RepositoryFactory


class PostgresRepositoryFactory(RepositoryFactory):
    """
    Concrete repository factory for PostgreSQL. Responsible for creating
    repositories that interface with PostgreSQL.
    """

    def __init__(self):
        self.connection_factory = PostgresConnectionFactory()

    def create_volumes_repository(self):
        """
        Create and return a PostgreSQL-specific VolumesRepository.
        """
        connection = self.connection_factory.get_connection()
        return VolumesRepository(connection)
