from fastapi import APIRouter, HTTPException
from factories.PostgresRepositoryFactory import PostgresRepositoryFactory
from factories.Neo4jRepositoryFactory import Neo4jRepositoryFactory
from RoutineGeneratorService import RoutineGenerator
from factories.CouchdbRepositoryFactory import CouchdbRepositoryFactory

router = APIRouter()

# Use the repository factory for Postgres volumes repository
repository_factory = PostgresRepositoryFactory()
volumes_repository = repository_factory.create_volumes_repository()
couchdb_repository_factory = CouchdbRepositoryFactory()

# Use the repository factory for Neo4j exercises repository
neo4j_repository_factory = Neo4jRepositoryFactory()
routine_generator = RoutineGenerator(repository_factory, neo4j_repository_factory)
exercises_repository = neo4j_repository_factory.create_exercises_repository()
routines_repository = couchdb_repository_factory.create_routines_repository()


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

@router.post("/routines/{user_id}")
async def create_routine(user_id: str, routine_data: dict):
    """
    Endpoint to save a new routine for a user.

    :param user_id: The user ID.
    :param routine_data: The routine details.
    """
    response = routines_repository.save_routine(user_id, routine_data)
    if response:
        return {"message": "Routine saved successfully.", "id": response}
    raise HTTPException(status_code=400, detail="Error saving routine.")


@router.get("/routines/{user_id}")
async def get_routines(user_id: str):
    """
    Endpoint to retrieve all routines for a user.

    :param user_id: The user ID.
    """
    routines = routines_repository.get_routines_by_user_id(user_id)
    if routines:
        return routines
    raise HTTPException(status_code=404, detail=f"No routines found for user {user_id}.")


@router.delete("/routines/{user_id}")
async def delete_routine(user_id: str):
    """
    Endpoint to delete a user's routine.

    :param user_id: The user ID.
    """
    success = routines_repository.delete_routine(user_id)
    if success:
        return {"message": "Routine deleted successfully."}
    raise HTTPException(status_code=404, detail=f"No routine found for user {user_id}.")

@router.get("/routine/{user_id}/{distribution_name}")
async def generate_and_save_routine(user_id: str, distribution_name: str):
    """
    Endpoint to generate a routine based on distribution and save it for a user.

    :param user_id: The ID of the user.
    :param distribution_name: The name of the distribution (e.g., push, pull, legs).
    :return: The generated routine.
    """
    try:
        # Step 1: Generate routine using RoutineGenerator
        routines = routine_generator.generate_routines(distribution_name)
        if not routines:
            raise HTTPException(status_code=404,
                                detail=f"No routines generated for distribution '{distribution_name}'.")

        # Step 2: Save routines to CouchDB for the user
        routine_data = {
            "user_id": user_id,
            "distribution_name": distribution_name,
            "routines": routines
        }
        response = routines_repository.save_routine(user_id, routine_data)
        return routine_data;

    except ValueError as error:
        # Specific handling for domain-specific errors
        raise HTTPException(status_code=400, detail=f"ValueError: {str(error)}")
    except HTTPException as http_error:
        # Allow already-raised HTTP exceptions to bubble up
        raise http_error
    except Exception as e:
        # Log and return a general 500 error
        print(f"Unexpected error during routine generation or saving: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")