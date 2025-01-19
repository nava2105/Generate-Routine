from abc import ABC, abstractmethod


class RepositoryFactory(ABC):
    """
    Abstract factory for repositories.
    """

    @abstractmethod
    def create_volumes_repository(self):
        """
        Create and return the volumes repository.
        """
        pass