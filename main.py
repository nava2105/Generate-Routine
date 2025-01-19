from fastapi import FastAPI
from controllers.RoutinesGeneratorController import router
from factories.PostgresConnectionFactory import PostgresConnectionFactory

app = FastAPI()

# Include the controller endpoints
app.include_router(router)


@app.on_event("startup")
async def startup_event():
    """
    Ensures the database schema and table exist by using the connection factory.
    """
    connection_factory = PostgresConnectionFactory()
    connection_factory.initialize_database()
