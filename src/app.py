from fastapi import FastAPI, Request
from starlette.middleware.gzip import GZipMiddleware

from .entrypoints import init_app
from .middleware import MessageLoggerMiddleware
from .routes import router

app = FastAPI(license_info={"name": "MIT"}, lifespan=init_app)

app.add_middleware(GZipMiddleware, compresslevel=7, minimum_size=700)
app.add_middleware(MessageLoggerMiddleware)


app.include_router(
    router,
)


@app.get("/helthzcheck")
def health_check(request: Request):
    """Health check endpoint for the API."""
    # TODO: Implement a proper health check that can retrieve
    # the status of the database and the usage of the service itself.
    request.state.logger.debug(
        "Call of the health check. All working fine",
    )
    return {"status": "ok", "message": "All working fine"}
