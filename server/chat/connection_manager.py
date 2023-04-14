from fastapi import WebSocket


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: dict[int, WebSocket] = {}

    async def connect(self, client_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        await self.broadcast(f"Client #{client_id} enter the chat")

    async def disconnect(self, client_id: int):
        self.active_connections.pop(client_id)
        await self.broadcast(f"Client #{client_id} left the chat")

    async def send_personal_message(self, client_id: int, message: str):
        websocket = self.active_connections[client_id]
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)
