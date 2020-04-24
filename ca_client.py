import socket
import select
import errno
import sys
import des
from des import DesKey
import time
from rsa import key, common, encrypt
from Crypto.PublicKey import RSA
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
from Crypto.PublicKey import DSA
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from des import DesKey
import des
# temp_key ='some key'
# encoded_key_c = temp_key.encode()
# key_tmp1 = DesKey(encoded_key_c)
import binascii

HEADER_LENGTH = 5000
IP = "127.0.0.1"
PORT = 1234
id_ca = 'ID_CA'
id_s = 'ID-Server'
ts2 = str(int(time.time()))

temp_key ='some key'
encoded_key_c = temp_key.encode()
key_tmp1 = DesKey(encoded_key_c) #key_temp1



key = RSA.generate(2048) #private key
private_key = key.exportKey()
ca_public_key = key.publickey().exportKey() #to bytes

s_key = RSA.generate(2048) #object private key
s_private_key = s_key.exportKey() #byte version of server private key
s_public_key = s_key.publickey().exportKey() #to bytes
# s_object_publickey = RSA.import_key(s_public_key) #object

f = open("file.txt", "wb")
f.write(ca_public_key)
f.close()


# CA = {'id_ca': 'ID_CA', 'pk_ca': pub_key, 'sk_ca': priv_key}


# user_input = input("Client: ") #asks for user input for identification
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #for streaming data
client_socket.connect((IP, PORT)) #client program is the one to connect while server binds

received_message = client_socket.recv(HEADER_LENGTH) #receives ktmpl, ids, ts1

decryptor = PKCS1_OAEP.new(key)
decrypted = decryptor.decrypt(received_message)
decoded_array = decrypted.decode("utf-8")

# key_tmp1 = decoded_array[0]

print(decoded_array)
print('Decrypted:', decrypted)



#STEP2
#cert_s = Sign_sk[id_s||id_ca||pk_s]
#CA-->S: DES_k_tmp1[pk_s||sk_s||cert_s||id_s||ts2]

s2_str = id_s + "|" + id_ca + "|"
s_object_pkey = RSA.import_key(s_public_key)
h = SHA256.new(s2_str.encode("utf-8"))
cert_s = pkcs1_15.new(key).sign(h)
print(type(cert_s))


concat = s_public_key + s_private_key + cert_s + id_s.encode("utf-8") + ts2.encode("utf-8")
print(type(key_tmp1))
des_encrypted = key_tmp1.encrypt(concat, padding=True)
cert_s_encrypted = key_tmp1.encrypt(cert_s, padding=True)
s_public_key_ecrypted = key_tmp1.encrypt(s_public_key, padding=True)


client_socket.send(des_encrypted)
client_socket.send(cert_s_encrypted)


client_socket.send(s_public_key)

# message = s2_str.encode("utf-8")



client_socket.close()

# #UI
# choose = input("Type create to make a new key or press enter to use already created key: ")
# if choose == "create":
#      input_key = input("Create a key: ")
#      encoded_key = input_key.encode()
#      print(encoded_key)
#      key = DesKey(encoded_key)
#      # print(key)
#      # f = open("key.txt", 'w')
#      # f.write(input_key)
#      # f.close()
# else:
#      input_key = input("Enter existing key: ")
#      encoded_key = input_key.encode()
#      print(encoded_key)
#      key = DesKey(encoded_key)
#
#
# recieve_header = client_socket.recv(HEADER_LENGTH)
#
# receive_length = int(recieve_header)
# #ticket_length = int(ticket_header.decode("utf-8").strip())
#
# receive_message = client_socket.recv(receive_length)
# print(receive_message) #encrypted ticket
#
#
# #While connected
# while True:
#
#     plain = input(f"{user_input} > ")
#
#     # ticket = client_socket.recv(ticket_length).decode("utf-8")
#     # print(ticket)
#
#     if plain:
#         new = plain.encode("utf-8")
#         message = key.encrypt(new, padding=True)
#         message_header = f"{len(message) :< {HEADER_LENGTH}}".encode("utf-8")
#         client_socket.send(message_header + message)
#
#
#     try:
#         while True:
#             #receive things
#
#             # decoded = key.decrypt(t, padding=True)
#
#
#             username_header = client_socket.recv(HEADER_LENGTH)
#             if not len(username_header):
#                 print("connection closed by the server")
#                 sys.exit()
#             username_length = int(username_header.decode("utf-8").strip())
#             username = client_socket.recv(username_length).decode("utf-8")
#
#             message_header = client_socket.recv(HEADER_LENGTH)
#             message_length = int(message_header.decode("utf-8").strip())
#             message = client_socket.recv(message_length)
#             decoded = key.decrypt(message, padding=True)
#             last = decoded.decode()
#
#             print(f" Username: {username}\n key: {key}\n Encrypted: {message}\n Decrypted: {last}\n ticket: {ticket}")
#
#     except IOError as e:
#         if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
#             print('Reading error', str(e))
#             sys.exit()
#         continue
#
#     except IOError as e:
#         print('General error', str(e))
#         sys.exit()