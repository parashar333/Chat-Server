import socket
import threading
clients = []
client_no = 0
connections = []
addresses = []

localhost = socket.gethostbyname(socket.gethostname())
port_no = 5566
Address = (localhost, port_no)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

def client_handle(connection, address):
    connections.append(connection)
    addresses.append(address)
    print(f"[NEW CONNECTION] {address} connected")
    connected = True
    while connected:
        print("connected" + "times")
        message = connection.recv(SIZE).decode(FORMAT)
        global client_no
        if message == DISCONNECT_MESSAGE:
            connected = False
            print(clients)
            for i in clients:
                keys = list(i.keys())
                if uniq_cli[0] in keys:
                   print("success")
                   del clients[clients.index(i)]
                   client_no = client_no - 1
        else:
            uniq_cli = str(address[1]).split(',')
            client_no += 1
            clients.append({uniq_cli[0]: client_no})
        print(clients)
        print(f"[{address}] {message}")  
        message = f"Message received: {message}"

        connection.sendall(message.encode(FORMAT))
        for i in addresses:
            print(i, "addresses")
            address.sendto(bytes(SIZE), i)
            # try:
            #     print(i, "connections")
            #     connection.sendto(message, i)
            # except:
            #     print("this connection is not present rn") 
    
    connection.close()

def main():
    print("Server is starting")
    soc_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc_server.bind(Address)
    soc_server.listen()
    print(f"[LISTENING] Server is listening on port {localhost}:{port_no}")

    while True:
        connection, address = soc_server.accept()
        thread = threading.Thread(target= client_handle, args= (connection, address))
        thread.start()
        print(f" [ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


if __name__ == "__main__":
    main()

# def threading_start(i):
#     print(i)


# localhost = "127.0.0.1"
# port_no = 1221

# soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# with soc:
#     soc.bind((localhost, port_no))
#     print("socket is listening to port")
#     soc.listen()
#     connection, address = soc.accept()
#     with connection:
#         print_lock.acquire()
#         print(f"connected to {address}")
#         thread_new = threading.Thread(threading_start(connection))
#         thread_new.start()
#         # while True:
#         #         data = connection.recv(1024)
#         #         if not data:
#         #             break
#         #         connection.sendall(data)
#     soc.close()