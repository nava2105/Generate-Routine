from neo4j import GraphDatabase


class ExercisesRepository:
    """
    Repository for interacting with Neo4j to fetch exercise data.
    """

    def __init__(self, driver: GraphDatabase.driver):
        """
        Initialize with a Neo4j driver.

        :param driver: Neo4j GraphDatabase driver instance.
        """
        self.driver = driver

    def get_exercises_by_muscle(self, muscle_name: str):
        """
        Retrieves exercises that work a specific muscle (directly or indirectly).

        :param muscle_name: The name of the muscle (e.g., 'chest').
        :return: A list of exercises related to the muscle.
        """
        with self.driver.session() as session:
            query = """
                MATCH (m:Muscle {name: $muscle_name})<-[:WORKS_DIRECTLY|WORKS_INDIRECTLY]-(e:Exercise)
                RETURN e.name AS exercise_name
            """
            result = session.run(query, muscle_name=muscle_name)
            exercises = [record["exercise_name"] for record in result]
            return exercises