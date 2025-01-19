from fastapi import APIRouter, HTTPException
from factories.PostgresRepositoryFactory import PostgresRepositoryFactory

router = APIRouter()

# Use the repository factory to create the repository instance
repository_factory = PostgresRepositoryFactory()
volumes_repository = repository_factory.create_volumes_repository()


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
