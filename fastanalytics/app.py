from fastapi import FastAPI, Request, status
from starlette.middleware.gzip import GZipMiddleware

from .entrypoints import init_app
from .middleware import MessageLoggerMiddleware
from .routes import router

app = FastAPI(license_info={"name": "MIT"}, lifespan=init_app)

app.add_middleware(MessageLoggerMiddleware)
app.add_middleware(GZipMiddleware, compresslevel=7, minimum_size=700)


app.include_router(
    router,
)


@app.api_route("/healthzcheck", methods=["GET", "HEAD"], status_code=status.HTTP_200_OK)
def health_check(request: Request) -> dict[str, str]:
    """Health check endpoint for the API."""
    # TODO: Implement a proper health check that can retrieve
    # the status of the database and the usage of the service itself.
    request.state.logger.debug(
        "Call of the health check. All working fine",
    )
    return {"status": "ok", "message": "All working fine"}
