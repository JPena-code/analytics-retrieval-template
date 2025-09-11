from fastapi import FastAPI

from .entrypoints import init_app
from .routes import router

app = FastAPI(license_info={"name": "MIT"}, lifespan=init_app)

app.include_router(
    router,
)


@app.get("/helthzcheck")
def health_check():
    """Health check endpoint for the API."""
    # TODO: Implement a proper health check that can retrieve
    # the status of the database and the usage of the service itself.
    return {"status": "ok"}
