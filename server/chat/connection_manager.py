from fastapi import WebSocket
from loguru import logger
from pydantic import ValidationError

from chat.models import ConnectionTransport, MessageType, Transport


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket) -> str:
        await websocket.accept()

        data = await websocket.receive_json()
        try:
            conn_transport = ConnectionTransport.parse_obj(data)
        except ValidationError as err:
            logger.exception(err)
            await websocket.close(4001, "Validation error")
            return ""

        nickname = conn_transport.nickname

        if nickname in self.active_connections:
            await websocket.close(4002, "Nickname already taken")
            return nickname
        
        chatters_list = list(self.active_connections.keys())
        transport = Transport(message_type=MessageType.CONNECTED, chatters=chatters_list)
        await websocket.send_text(transport.json())

        self.active_connections[nickname] = websocket

        transport = Transport(message_type=MessageType.CONNECT, nickname=nickname)
        await self.broadcast_except_sender(nickname, transport)

        return nickname

    async def disconnect(self, nickname: str):
        self.active_connections.pop(nickname)
        data = Transport(message_type=MessageType.DISCONNECT, nickname=nickname)
        await self.broadcast(data)

    async def personal_message(self, nickname: str, transport: Transport):
        await self.active_connections[nickname].send_text(transport.json())

    async def broadcast(self, transport: Transport):
        for connection in self.active_connections.values():
            await connection.send_text(transport.json())

    async def broadcast_except_sender(self, nickname: str, transport: Transport):
        for nick, connection in self.active_connections.items():
            if nick != nickname:
                await connection.send_text(transport.json())
