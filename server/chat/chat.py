from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from fastapi.websockets import WebSocketState
from loguru import logger

from chat.connection_manager import ConnectionManager
from chat.models import Transport


chat_router = APIRouter()

manager = ConnectionManager()

templates = Jinja2Templates(directory="templates")


@chat_router.get("/")
async def get(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


@chat_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    nickname = await manager.connect(websocket)

    logger.debug(websocket.application_state)
    if websocket.application_state == WebSocketState.DISCONNECTED:
        return
    try:
        while True:
            data = await websocket.receive_text()
            logger.debug(data)
            obj = Transport.parse_raw(data)
            await manager.broadcast_except_sender(nickname, obj)
    except WebSocketDisconnect:
        await manager.disconnect(nickname)
