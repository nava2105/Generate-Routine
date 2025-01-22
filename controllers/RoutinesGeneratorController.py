from fastapi import APIRouter, HTTPException
from factories.PostgresRepositoryFactory import PostgresRepositoryFactory
from factories.Neo4jRepositoryFactory import Neo4jRepositoryFactory
from RoutineGeneratorService import RoutineGenerator

router = APIRouter()

# Use the repository factory for Postgres volumes repository
repository_factory = PostgresRepositoryFactory()
volumes_repository = repository_factory.create_volumes_repository()

# Use the repository factory for Neo4j exercises repository
neo4j_repository_factory = Neo4jRepositoryFactory()
routine_generator = RoutineGenerator(repository_factory, neo4j_repository_factory)
exercises_repository = neo4j_repository_factory.create_exercises_repository()


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/volume/{muscle_name}")
async def get_volume(muscle_name: str):
    """
    Endpoint to fetch training volume information for a specific muscle group.
    """
    volume_data = volumes_repository.get_volume_by_muscle_name(muscle_name)
    if volume_data:
        return volume_data
    raise HTTPException(status_code=404, detail=f"Muscle group '{muscle_name}' not found.")


@router.get("/exercises/{muscle_name}")
async def get_exercises(muscle_name: str):
    """
    Endpoint to fetch exercises for a specific muscle group.
    """
    exercises = exercises_repository.get_exercises_by_muscle(muscle_name)
    if exercises:
        return exercises
    raise HTTPException(status_code=404, detail=f"No exercises found for muscle group '{muscle_name}'.")


@router.get("/muscles_by_group/{group_name}")
async def get_muscles_by_group(group_name: str):
    """
    Endpoint to fetch muscles associated with a specific group.
    """
    muscles_by_group = exercises_repository.get_muscles_by_group(group_name)
    if muscles_by_group:
        return muscles_by_group
    raise HTTPException(status_code=404, detail=f"No muscles found for group '{group_name}'.")


@router.get("/groups_by_distribution/{distribution_name}")
async def get_groups_by_distribution(distribution_name: str):
    """
    Endpoint to fetch groups associated with a specific distribution.
    """
    groups_by_distribution = exercises_repository.get_groups_by_distribution(distribution_name)
    if groups_by_distribution:
        return groups_by_distribution
    raise HTTPException(status_code=404, detail=f"No groups found for distribution '{distribution_name}'.")


@router.get("/routine/{distribution_name}")
async def get_routine(distribution_name: str):
    try:
        routines = routine_generator.generate_routines(distribution_name)
        print("Generated Routines:")
        list_of_routines = []
        for routine in routines:
            print(routine)
            list_of_routines.append(routine)
    except ValueError as error:
        print(f"Error: {error}")
        raise HTTPException(status_code=404, detail=error.args[0])
    return list_of_routines
