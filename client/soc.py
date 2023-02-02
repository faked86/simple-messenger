import socketio


sio_client = socketio.Client()


@sio_client.event
def connect():
    print('Connection established.')


@sio_client.event
def message_from_server(data):
    print(f"Recieved message: {data}")
    print()
    print("Your message: ")


@sio_client.event
def disconnect():
    print('\nDisconnected from server.')