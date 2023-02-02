from client.soc import sio_client


def main():
    sio_client.connect('http://localhost:8000', socketio_path="sockets")
    print("Start chatting:")
    while True:
        try:
            message = input("Your message: \n")
            sio_client.emit("message_from_client", message)
        except:
            sio_client.disconnect()
            break


if __name__ == '__main__':
    main()
