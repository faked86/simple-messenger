from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates

from server.chat.connection_manager import ConnectionManager


chat_router = APIRouter()

manager = ConnectionManager()

templates = Jinja2Templates(directory="server/templates")


@chat_router.get("/")
async def get(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


@chat_router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
