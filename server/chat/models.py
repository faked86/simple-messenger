import json
from enum import Enum, auto

from pydantic import BaseModel, ValidationError


class MessageType(str, Enum):
    CONNECT = "CONNECT"
    DISCONNECT = "DISCONNECT"
    MESSAGE = "MESSAGE"
    PICTURE = "PICTURE"


class User(BaseModel):
    client_id: int
    nickname: str


class Transport(BaseModel):
    message_type: MessageType
    client_id: int
    nickname: str
    message: str
    picture: bytes


class ConnectionTransport(BaseModel):
    nickname: str


if __name__ == "__main__":
    usr = {
        "client_id": 1,
        # "nickname": "Dan",
        "a": 1
    }
    s = json.dumps(usr)

    try:
        u = User.parse_raw(s)
        print(u)
    except ValidationError as err:
        print(err)
