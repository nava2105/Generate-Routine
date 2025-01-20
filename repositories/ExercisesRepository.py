from neo4j import GraphDatabase


class ExercisesRepository:
    """
    Repository for interacting with Neo4j to fetch exercise, muscle, and group data.
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
                MATCH (m:Muscle {name: $muscle_name})-[:WORKS_DIRECTLY]-(e:Exercise)
                RETURN e.name AS exercise_name
            """
            result = session.run(query, muscle_name=muscle_name)
            exercises = [record["exercise_name"] for record in result]
            return exercises

    def get_muscles_by_group(self, group_name: str):
        """
        Retrieves all muscles for a specific group.

        :param group_name: The name of the group to filter (e.g., 'push').
        :return: A list of muscles associated with the group.
        """
        with self.driver.session() as session:
            query = """
                MATCH (g:Group {name: $group_name})-[:INCLUDES]->(m:Muscle)
                RETURN m.name AS muscles
            """
            result = session.run(query, group_name=group_name)
            muscles_by_group = [record["muscles"] for record in result]
            return muscles_by_group

    def get_groups_by_distribution(self, distribution_name: str):
        """
        Retrieves all groups for a specific distribution.

        :param distribution_name: The name of the distribution to filter (e.g., 'full body').
        :return: A list of groups associated with the distribution.
        """
        with self.driver.session() as session:
            query = """
                MATCH (d:Distribution {name: $distribution_name})-[:USES]->(g:Group)
                RETURN g.name AS groups
            """
            result = session.run(query, distribution_name=distribution_name)
            groups_by_distribution = [record["groups"] for record in result]
            return groups_by_distribution
