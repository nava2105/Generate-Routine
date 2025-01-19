from repositories.ExercisesRepository import ExercisesRepository
from config.Neo4jConfig import Neo4jConfig


class Neo4jRepositoryFactory:
    """
    Factory to create Neo4j-specific repositories.
    """

    def __init__(self):
        """
        Initializes the repository factory with a Neo4jConfig instance.
        """
        self.config = Neo4jConfig()  # Manages the Neo4j database connection.

    def create_exercises_repository(self):
        """
        Creates and returns the ExercisesRepository.
        
        :return: An instance of ExercisesRepository.
        """
        return ExercisesRepository(self.config.get_driver())

    def close(self):
        """
        Closes the Neo4j connection when the factory is destroyed.
        """
        self.config.close()