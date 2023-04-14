from fastapi import FastAPI

from chat.chat import chat_router

app = FastAPI(
    title="Simple social network",
)


def create_app() -> FastAPI:
    app.include_router(chat_router)
    return app
