import json

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: dict[int, WebSocket] = {}

    async def connect(self, client_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[client_id] = websocket

        data = await websocket.receive_json()
        await self.broadcast(json.dumps(data))

    async def disconnect(self, client_id: int):
        self.active_connections.pop(client_id)
        data = {
            "client_id": client_id,
            "nickname": "nickname",
            "message": "left the chat",
            "picture": None
        }
        await self.broadcast(json.dumps(data))

    async def send_personal_message(self, client_id: int, message: str):
        websocket = self.active_connections[client_id]
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)
