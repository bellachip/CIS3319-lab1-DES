import socket
import select
import errno
import sys
import des
from des import DesKey
import time

HEADER_LENGTH = 1024
IP = "127.0.0.1"
PORT =  1234

idc = 'CIS3319USERID'
idv = 'CIS3319SERVERID'
idtgs = 'CIS3319TGSID'
adc = IP + ':' + str(PORT)
ts = str(int(time.time()))

request_ticket = idc + '|' + idv + '|'+ ts




user_input = input("Client: ") #asks for user input for identification
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #for streaming data
client_socket.connect((IP, PORT)) #client program is the one to connect while server binds
client_socket.setblocking(False) #sets blocking to



user_id = user_input.encode("utf-8") #always has to translate to uit-8
username_header = f"{len(user_id):<{HEADER_LENGTH}}".encode("utf-8")
client_socket.send(username_header + user_id)


encoded_request_ticket = request_ticket.encode("utf-8")
print(encoded_request_ticket)
message_header = f"{len(encoded_request_ticket) :< {HEADER_LENGTH}}".encode("utf-8")
client_socket.send(message_header + encoded_request_ticket)

# ticket = client_socket.recv(1024)
# print(ticket)


#UI
choose = input("Type create to make a new key or press enter to use already created key: ")
if choose == "create":
     input_key = input("Create a key: ")
     encoded_key = input_key.encode()
     print(encoded_key)
     key = DesKey(encoded_key)
     # print(key)
     # f = open("key.txt", 'w')
     # f.write(input_key)
     # f.close()
else:
     input_key = input("Enter existing key: ")
     encoded_key = input_key.encode()
     print(encoded_key)
     key = DesKey(encoded_key)

#While connected
while True:
    plain = input(f"{user_input} > ")
    ticket_header = client_socket.recv(HEADER_LENGTH)
    ticket_length = int(ticket_header.decode("utf-8").strip())
    ticket = client_socket.recv(ticket_length).decode("utf-8")
    print(ticket)

    if plain:
        new = plain.encode("utf-8")
        message = key.encrypt(new, padding=True)
        message_header = f"{len(message) :< {HEADER_LENGTH}}".encode("utf-8")
        client_socket.send(message_header + message)


    try:
        while True:
            #receive things

            # decoded = key.decrypt(t, padding=True)


            username_header = client_socket.recv(HEADER_LENGTH)
            if not len(username_header):
                print("connection closed by the server")
                sys.exit()
            username_length = int(username_header.decode("utf-8").strip())
            username = client_socket.recv(username_length).decode("utf-8")

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode("utf-8").strip())
            message = client_socket.recv(message_length)
            decoded = key.decrypt(message, padding=True)
            last = decoded.decode()

            print(f" Username: {username}\n key: {key}\n Encrypted: {message}\n Decrypted: {last}\n ticket: {ticket}")

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error', str(e))
            sys.exit()
        continue

    except IOError as e:
        print('General error', str(e))
        sys.exit()