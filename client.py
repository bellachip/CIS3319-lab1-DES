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

user_input = input("Client: ")  # asks for user input for identification
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # for streaming data
client_socket.connect((IP, PORT))  # client program is the one to connect while server binds
client_socket.setblocking(False)  # sets blocking to FALSE

user_id = user_input.encode("utf-8")  # always has to translate to uit-8
username_header = f"{len(user_id):<{HEADER_LENGTH}}".encode("utf-8")
client_socket.send(username_header + user_id)
# UI
choose = input("Type create to make a new key or press enter to use already created key: ")
if choose == "create":
    input_deskey = input("Create a deskey: ")
    encoded_deskey = input_deskey.encode()
    print(encoded_deskey)
    key = DesKey(encoded_deskey)
    input_hmackey = input("Create a hamc key: ")
    encoded_hmackey = bytes(input_hmackey, 'utf-8')

    # print(key)
    # f = open("key.txt", 'w')
    # f.write(input_key)
    # f.close()
else:
    input_deskey = input("Enter existing deskey: ")
    encoded_deskey = input_deskey.encode()
    print(encoded_deskey)
    key = DesKey(encoded_deskey)
    input_hmackey = input("Enter existing hmac key: ")
    encoded_hmackey = bytes(input_hmackey, 'utf-8')

hash_length = 0
# While connected
while True:
    plain = input(f"{user_input} > ")

    if plain:
        new = plain.encode("utf-8")
        # hashkey = bytes("hello", "utf-8")
        # hash
        hash = hmac.new(encoded_hmackey, new, hashlib.sha256)
        digested_hash = hash.digest()
        encoded_hash = base64.b64encode(digested_hash)

        message2 = key.encrypt(new, padding=True)
        delimeter = bytes("#", "utf-8")
        # print("Encrypted message")
        # print(message2)

        message = message2 + delimeter + encoded_hash
        # print("Message with Hash in bytes")
        # print(message)
        message_header = f"{len(message) :< {HEADER_LENGTH}}".encode("utf-8")
        client_socket.send(message_header + message)
    try:
        while True:
            # receive things
            username_header = client_socket.recv(HEADER_LENGTH)
            if not len(username_header):
                print("connection closed by the server")
                sys.exit()
            username_length = int(username_header.decode("utf-8").strip())
            username = client_socket.recv(username_length).decode("utf-8")

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode("utf-8").strip())
            message = client_socket.recv(message_length)
            print("message inside the try in bytes")
            print(message)

            array = message.split(b'#')
            HMAC = array[1]
            encrypted_message = array[0]

            decoded = key.decrypt(encrypted_message, padding=True)
            hash = hmac.new(encoded_hmackey, decoded, hashlib.sha256)
            digested_hash = hash.digest()
            encoded_hash = base64.b64encode(digested_hash)
            last = decoded.decode()

            retval =hmac.compare_digest(encoded_hash, HMAC)



            print(
                f" Username: {username}\n Deskey: {key}\n HashKey: {encoded_hmackey}\n HMAC: {HMAC}\n Encrypted: {encrypted_message}\n Decrypted: {last}\n Encoded Hash: {encoded_hash}\n ReturnValueForHash: {retval}\n")

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error', str(e))
            sys.exit()
        continue

    except IOError as e:
        print('General error', str(e))
        sys.exit()
