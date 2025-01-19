from fastapi import APIRouter, HTTPException
from factories.PostgresRepositoryFactory import PostgresRepositoryFactory
from factories.Neo4jRepositoryFactory import Neo4jRepositoryFactory

router = APIRouter()

# Use the repository factory for Postgres volumes repository
repository_factory = PostgresRepositoryFactory()
volumes_repository = repository_factory.create_volumes_repository()

# Use the repository factory for Neo4j exercises repository
neo4j_repository_factory = Neo4jRepositoryFactory()
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
