import socket
import select

HEADER_LENGTH = 1024
ip = "127.0.0.1"
port = 8080
count = 0

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((ip, port)) 
server_socket.listen()

sockets_list = [server_socket]

clients = {}

def receive_msg(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)
        message_length = int(message_header.decode("utf-8").strip())
        return {"header": message_header, "data": client_socket.recv(message_length)}
    except Exception as e:
        return False

while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notif_sockets in read_sockets:
        if notif_sockets == server_socket:
            client_socket, client_address = server_socket.accept()

            user = receive_msg(client_socket)
            if user is False:
                continue

            sockets_list.append(client_socket)

            clients[client_socket] = user

            print(f"New connection from {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')}")

        else:
            message = receive_msg(notif_sockets)

            if message is False:
                if count !=1:
                    print(f"Closed connection from {clients[notif_sockets]['data'].decode('utf-8')}")
                    sockets_list.remove(notif_sockets)
                    for client_socket in clients:
                        if client_socket != notif_sockets:
                            client_socket.send(user['data'] + ' lost connection'.encode('utf-8'))
                    del clients[notif_sockets]
                    count = 0
                    continue
                else:
                    print(f"Closed connection from {clients[notif_sockets]['data'].decode('utf-8')}")
                    sockets_list.remove(notif_sockets)
                    del clients[notif_sockets]
                    count = 0
                    continue 

            user = clients[notif_sockets]
            print(f"Recieved message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")

            if "/quit" in message['data'].decode('utf-8'):
                count+=1
                print(f"Closed connection from {clients[notif_sockets]['data'].decode('utf-8')}")
                for client_socket in clients:
                        if client_socket != notif_sockets:
                            client_socket.send(user['data'] + ' is quitting'.encode('utf-8')) 

            if "/bc" in message['data'].decode('utf-8'):
                msg = message['data'].decode('utf-8')
                msg = message['data'].decode('utf-8').split("/bc ")[1]
                for client_socket in clients:
                    if client_socket != notif_sockets:
                        client_socket.send(user['header'] + user['data'] + message['header'] + msg.encode('utf-8'))
            
            if "/dm" in message['data'].decode('utf-8'):
                client_count = 0
                for i in clients:
                    substr = clients[i]['data'].decode('utf-8').split("'")[0]
                    substr1 = message['data'].decode('utf-8').split("/dm ")
                    substr1 = substr1[1].split(" ",1)
                    if substr1[0] == substr and substr1[0] != user['data'].decode('utf-8').split("b")[0]:
                        client_count+=1
                        i.send(user['data'] + '  >  '.encode('utf-8') + substr1[1].encode('utf-8'))
                        break
                if client_count == 0:
                    print(substr1[0] + "does not exist")
                    for client_socket in clients:
                        if client_socket == notif_sockets:
                            client_socket.send((substr1[0] + " does not exist").encode('utf-8'))

            if "/users" in message['data'].decode('utf-8'):
                users_list=[]
                for i in clients:
                    substr = clients[i]['data'].decode('utf-8').split("'")[0]
                    users_list.append(substr)
                users_list = ' , '.join(users_list)
                for client_socket in clients:
                    if client_socket == notif_sockets:
                        if "/users" in message['data'].decode('utf-8'):
                            client_socket.send(users_list.encode('utf-8'))
                        else:
                            client_socket.send("help".encode('utf-8'))

            if "/help" in message['data'].decode('utf-8'):
                users_list=[]
                for i in clients:
                    substr = clients[i]['data'].decode('utf-8').split("'")[0]
                    users_list.append(substr)
                users_list = ' , '.join(users_list)
                for client_socket in clients:
                    if client_socket == notif_sockets:
                        if "/users" in message['data'].decode('utf-8'):
                            client_socket.send(users_list.encode('utf-8'))
                        else:
                            client_socket.send("help".encode('utf-8'))
                    
    for notif_sockets in exception_sockets:
        sockets_list.remove(notif_sockets)
        del clients[notif_sockets]