import socket

localhost = socket.gethostbyname(socket.gethostname())
port_no = 5566
Address = (localhost, port_no)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(Address)
    print(f"[CONNECTED] Client connected to server at {localhost}:{port_no}")

    connected = True
    while connected:
        message = input("> ")

        client.send(message.encode(FORMAT))

        if message == DISCONNECT_MESSAGE:
            connected = False
        else:
            message = client.recv(SIZE).decode(FORMAT)
            print(f"[SERVER] {message}")


if __name__ == "__main__":
    main()