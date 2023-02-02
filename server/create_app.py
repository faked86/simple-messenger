from fastapi import FastAPI

from server.api.auth.views import auth_router
from server.api.sockets import sio_app


app = FastAPI(
    title="Simple social network",
)


def create_app() -> FastAPI:
    app.include_router(auth_router)
    app.mount("/", app=sio_app)
    return app
