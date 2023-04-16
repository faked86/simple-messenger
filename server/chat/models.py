from enum import Enum

from pydantic import BaseModel


class MessageType(str, Enum):
    CONNECTED = "CONNECTED"
    CONNECT = "CONNECT"
    DISCONNECT = "DISCONNECT"
    MESSAGE = "MESSAGE"
    PICTURE = "PICTURE"


class Transport(BaseModel):
    message_type: MessageType
    nickname: str | None = None
    text: str | None = None
    picture: bytes | None = None
    chatters: list[str] | None = None


class ConnectionTransport(BaseModel):
    nickname: str
