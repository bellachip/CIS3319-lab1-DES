import base64
import hmac
import socket
import select
import errno
import sys
import des
from des import DesKey
import hashlib

HEADER_LENGTH = 1024
IP = "127.0.0.1"
PORT = 1234

user_input = input("Client: ") #asks for user input for identification
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #for streaming data
client_socket.connect((IP, PORT)) #client program is the one to connect while server binds
client_socket.setblocking(False) #sets blocking to FALSE

user_id = user_input.encode("utf-8") #always has to translate to uit-8
username_header = f"{len(user_id):<{HEADER_LENGTH}}".encode("utf-8")
client_socket.send(username_header + user_id)
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

hash_length = 0
#While connected
while True:
    plain = input(f"{user_input} > ")

    if plain:
        new = plain.encode("utf-8")
        hashkey = bytes("the shared secret key here", "utf-8")
        #hash
        hash = hmac.new(hashkey, new, hashlib.sha256)
        digested_hash = hash.digest()
        encoded_hash = base64.b64encode(digested_hash)

        message2 = key.encrypt(new, padding=True)
        delimeter =bytes("#", "utf-8")
        print("Encrypted message")
        print(message2)
        message = message2 + delimeter + encoded_hash
        print("Message with Hash")
        print(message)
        message_header = f"{len(message) :< {HEADER_LENGTH}}".encode("utf-8")
        client_socket.send(message_header + message)
    try:
        while True:
            #receive things
            username_header = client_socket.recv(HEADER_LENGTH)
            if not len(username_header):
                print("connection closed by the server")
                sys.exit()
            username_length = int(username_header.decode("utf-8").strip())
            username = client_socket.recv(username_length).decode("utf-8")

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode("utf-8").strip())
            message = client_socket.recv(message_length)
            print("message inside the try")
            string = str(message)
            splitted = string.split("#")
            print("string array")
            print(splitted)

            ready = splitted[0]
            print("ready")
            print(ready)
            lol = str(ready)
            print("lol")
            print(lol)
            lol_quote = lol + "'"
            print("lol_quote")
            print(lol_quote)
            enc = lol_quote.encode()
            print("enc")
            print(enc)

            check1 = enc.replace('"', '')
            print("check1")
            print(check1)

            length = len(ready)
            # next = ready[:length]
            # print("new next")
            # print(next)
            # add_single_quote =
            decoded = key.decrypt(new_bytes, padding=True)

            last = decoded.decode()
            print(f" Username: {username}\n key: {key}\n Encrypted: {message}\n Decrypted: {last}\n")

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error', str(e))
            sys.exit()
        continue

    except IOError as e:
        print('General error', str(e))
        sys.exit()