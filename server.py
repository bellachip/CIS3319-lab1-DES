import socket
import select
#server


HEADER_LENGTH = 10
IP = "127.0.0.1" #dummy ipaddress"
PORT = 1234 #dummy port

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creating socket
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #allows to reconnect
server_socket.bind((IP, PORT)) #server program binds with the right ip and port
server_socket.listen() #listend

sockets_list = [server_socket] #for client list

clients = {} #clents list for client info

#recienve message from any client socket
def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH) #first receive what ever the header length is
        if not len(message_header): #if not recieve any data then the client close the connection
            return False
        message_length = int(message_header.decode("utf-8").strip()) #otherwise get the message (always have to decode)
        return {"header": message_header, "data": client_socket.recv(message_length)} #returning a dictionary where the values are header, data
    except:
        return False


while True:
    #third param= error socket
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list) #first param is the sockets we are going to read in

    for notified_socket in read_sockets:
        if notified_socket == server_socket: #client just connected therefore accept the connection
            client_socket, client_address = server_socket.accept()

            user = receive_message(client_socket) #receive message for current client socket
            if user is False: #disconnceted
                continue

            sockets_list.append(client_socket)
            clients[client_socket] = user
            ip = client_address[0] #client ip address
            client_port = client_address[1] #port number
            print(
                f"Accepted new connection from {ip}: {client_port} username:{user['data'].decode('utf-8')}")
        else:
            message = receive_message(notified_socket)
            if message is False:
                print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            user = clients[notified_socket]

            print(f"Received message from {user['data'].decode('utf-8')}: {message['data']}")

            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
            for notified_socket in exception_sockets:
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
