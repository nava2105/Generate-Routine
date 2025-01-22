from fastapi import APIRouter, HTTPException, Depends
from factories.PostgresRepositoryFactory import PostgresRepositoryFactory
from factories.Neo4jRepositoryFactory import Neo4jRepositoryFactory
from services.RoutineGeneratorService import RoutineGenerator
from factories.CouchdbRepositoryFactory import CouchdbRepositoryFactory
from services.AuthService import authenticate_user

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


@router.get("/get/routines")
async def get_routines(user_id: int = Depends(authenticate_user)):
    """
    Endpoint to retrieve all routines for a user.

    :param user_id: The user ID.
    """
    routines = routines_repository.get_routines_by_user_id(user_id)
    if routines:
        return routines
    raise HTTPException(status_code=404, detail=f"No routines found for user {user_id}.")


@router.post("/create/routines/{distribution_name}")
async def generate_and_save_routine(distribution_name: str, user_id: int = Depends(authenticate_user)):
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
        return routine_data

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