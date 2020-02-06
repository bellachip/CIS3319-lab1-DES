import socket
import select
import errno
import sys
import des
from des import DesKey

HEADER_LENGTH = 30
IP = "127.0.0.1"
PORT = 1234

user_input = input("Client: ")  # asks for user input for identification
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # for streaming data
client_socket.connect((IP, PORT))  # client program is the one to connect while server binds
client_socket.setblocking(False)  # sets blocking to FALSE

user_id = user_input.encode("utf-8")  # always has to translate to uit-8
username_header = f"{len(user_id) :< {HEADER_LENGTH}}".encode("utf-8")
client_socket.send(username_header + user_id)

#UI
choose = input("Type create to make a new key or press enter to use already created key: ")
if choose == "create":
    input_key = input("Create a key: ")
    encoded_key = input_key.encode()
    print(encoded_key)
    key = DesKey(encoded_key)
else:
    input_key = input("Enter existing key: ")
    encoded_key = input_key.encode()
    print(encoded_key)
    key = DesKey(encoded_key)

# While connected

while True:

    message = input(f"{user_input} > ")
    print(message)
    if message:
        message = message.encode("utf-8")
        message_header = f"{len(message) :< {HEADER_LENGTH}}".encode("utf-8") #this is the one that is adding one space before the length of the message recienved
        print(message_header)
        print(message)
        client_socket.send(message_header + message)
    try:
        while True:
            # receive things
            username_header = client_socket.recv(HEADER_LENGTH)
            if not len(username_header):
                print("Connection Closed by the Server")
                sys.exit()
            username_length = int(username_header.decode("utf-8").strip())
            username = client_socket.recv(username_length).decode("utf-8")

            message_header = client_socket.recv(HEADER_LENGTH)

            a = bytearray(message_header)
            del a[0]
            #print(a)
            b = bytes(a)
            #print(b.strip())
            # string = str(message_header, 'utf-8')
            # print(string)
            # print(string[1:])
            message_length = len(message_header)
            #print(message_length)
            message = client_socket.recv(message_length).decode("utf-8")  # decodes to string
            print(f"{username} > {message}")

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error', str(e))
            sys.exit()
        continue

    except IOError as e:
        print('General error', str(e))
        sys.exit()
