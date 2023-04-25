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
        # client.sendall(str.encode("\n".join([str(message), str(port_no)])))

        if message == DISCONNECT_MESSAGE:
            connected = False
        else:
            message = client.recv(SIZE).decode(FORMAT)
            print(f"[SERVER] {message}")


if __name__ == "__main__":
    main()

# import socket

# local_host = "127.0.0.1"
# port_no = 1221

# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# with sock:
#     sock.connect((local_host,port_no))
#     sock.sendall(b"Hello server this is client")
#     data = sock.recv(1024)

# print(f"Received {data.decode('utf-8')}")