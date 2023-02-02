import socketio
from loguru import logger

from server.db.session import get_session
from server.oauth2.core import get_current_user

sio_server = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=[]
)

sio_app = socketio.ASGIApp(
    socketio_server=sio_server,
    socketio_path="sockets"
)


@sio_server.event
async def connect(sid, env, auth):
    logger.debug(f"{sid} connected.")

    # db_session_gen = get_session()
    # user = await get_current_user(auth["Authorization"], next(db_session_gen))

    await sio_server.emit("message_from_server", f"{sid} connected.", skip_sid=sid)


@sio_server.event
async def disconnect(sid):
    logger.debug(f"{sid} disconnected.")


@sio_server.event
async def message_from_client(sid, message):
    logger.debug(f"{sid} sent: {message}")
    await sio_server.emit("message_from_server", message, skip_sid=sid)
