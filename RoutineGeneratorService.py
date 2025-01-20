from factories.Neo4jRepositoryFactory import Neo4jRepositoryFactory
from factories.PostgresRepositoryFactory import PostgresRepositoryFactory


class RoutineGenerator:
    """
    Class to generate training routines based on distribution and muscle volumes
    from PostgreSQL and Neo4j exercises.
    """

    def __init__(self, postgres_factory: PostgresRepositoryFactory, neo4j_factory: Neo4jRepositoryFactory):
        """
        Initialize with repository factories for PostgreSQL and Neo4j.

        :param postgres_factory: A factory for creating PostgreSQL repositories.
        :param neo4j_factory: A factory for creating Neo4j repositories.
        """
        self.volumes_repository = postgres_factory.create_volumes_repository()
        self.groups_repository = neo4j_factory.create_exercises_repository()

    def generate_routines(self, distribution_name: str, days_per_week: int):
        """
        Generates workout routines for a given distribution and number of training days.

        :param distribution_name: The name of the distribution (e.g., "push, pull, legs").
        :param days_per_week: The number of days per week to train.
        :return: A list of routines, where each routine corresponds to a training day.
        """
        # Step 1: Get all groups in the distribution
        groups = self.groups_repository.get_groups_by_distribution(distribution_name)
        if not groups:
            raise ValueError(f"No groups found for distribution '{distribution_name}'.")

        # Validate the number of days matches the number of groups
        if len(groups) != days_per_week:
            raise ValueError(
                f"The number of training days ({days_per_week}) must equal the number of groups in the distribution ({len(groups)})."
            )

        # Step 2: Generate routines for each group
        routines = []
        for group in groups:
            # Fetch the muscles in the group
            muscles = self.groups_repository.get_muscles_by_group(group_name=group)
            if not muscles:
                continue

            # Create routine for each day
            routine = {"day": len(routines) + 1, "group": group, "exercises": []}

            for muscle in muscles:
                # Get MEV (total sets) for the muscle
                volume_data = self.volumes_repository.get_volume_by_muscle_name(muscle)
                if not volume_data or "mev" not in volume_data:
                    continue  # Skip if no MEV is available
                mev = volume_data["mev"]

                # Get up to 4 exercises for the muscle
                exercises = self.groups_repository.get_exercises_by_muscle(muscle_name=muscle)[:4]
                if not exercises:
                    continue

                # Decide the number of exercises to distribute MEV
                num_exercises = min(len(exercises), mev // 3 or 1)

                # Distribute MEV across chosen exercises
                base_sets = mev // num_exercises
                remainder = mev % num_exercises

                for i, exercise in enumerate(exercises[:num_exercises]):
                    sets = base_sets + (1 if i < remainder else 0)  # Evenly distribute remaining sets
                    routine["exercises"].append({
                        "muscle": muscle,
                        "exercise": exercise,
                        "sets": sets,
                    })

            # Add the routine for this group to the list
            routines.append(routine)

        return routines
