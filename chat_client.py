import socket
import errno
import sys

HEADER_LENGTH = 1024
ip = "127.0.0.1"
port = 8080
help_msgcontent=''' Help command : (Syntax - /help) - This command should print out a list of all supported commands and their behaviors. 
                Users command : (Syntax - /users) - This command should request a list of users from the server and then print out their names.
                Direct Message command : (Syntax - /dm username "message") - This command should send the message between quotes to the specified user. The client will make the request to the server.
                Broadcast command : (Syntax - /bc "message") - This command should send the message between quotes to all other connected users. The client will make the request to the server.
                Quit command : (Syntax - /quit) - Disconnect from the server. Before disconnecting, send a message to the server saying you will disconnect.'''

ip_no = input("IP: ")
port_no = input("Portno: ")

user_name = input("Username: ")
if ip_no == ip and port_no == str(port) and len(user_name)>0:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))
    client_socket.setblocking(False)
else:
    print("Enter expected inputs, correct portno,ip and username length should be greater than zero")
    sys.exit()
username = user_name.encode("utf-8")
username_header = f"{len(username):<{HEADER_LENGTH}}".encode("utf-8")
client_socket.send(username_header + username)

while True:
    message = input(f"{user_name} > ")

    if message == "/quit":
        message = message.encode("utf-8")
        message_header = f"{len(message):< {HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)
        sys.exit()

    elif message:
        message = message.encode("utf-8")
        message_header = f"{len(message):< {HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)

    try:
        while True:
            username_header = client_socket.recv(HEADER_LENGTH)
            if not len(username_header):
                print("Connection closed by the server")
                sys.exit()
            username_length = int(username_header.decode("utf-8").strip())
            username = client_socket.recv(username_length).decode("utf-8")

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode("utf-8").strip())
            message = client_socket.recv(message_length).decode("utf-8")

            print(f"{username} > {message}")

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error', str(e))
            sys.exit()
        continue

    except Exception as e:
        if str(e).split(':',1)[1].strip().split("'")[1] == 'help':
            print(help_msgcontent)
            e = ""
        else:
            print(str(e).split(':',1)[1].strip())
            e = ""

