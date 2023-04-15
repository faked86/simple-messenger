from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from chat.chat import chat_router

app = FastAPI(
    title="Simple social network",
)


def create_app() -> FastAPI:
    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.include_router(chat_router)
    return app
