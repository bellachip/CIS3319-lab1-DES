import socket
import select
import errno
import sys
import des
from des import DesKey
import time
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
import binascii
from Crypto.Hash import SHA256
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from rsa import key, common, encrypt

HEADER_LENGTH = 5000
IP = "127.0.0.1"
PORT =  1234
id_s = 'ID-Server'
ts3 = str(int(time.time()))
id_c = 'ID-Client'


temp_key ='some key'
encoded_key_2 = temp_key.encode()
key_tmp2 = DesKey(encoded_key_2) #key_temp1


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #for streaming data
client_socket.connect((IP, PORT)) #client program is the one to connect while server binds

step3 = id_s.encode("utf-8") + ts3.encode("utf-8")
client_socket.send(step3)


step4 = client_socket.recv(HEADER_LENGTH)
print(step4)

pk_s =client_socket.recv(HEADER_LENGTH)
print( "here is the pks")
print(type(pk_s))

object_pk_s = RSA.import_key(pk_s) #object

ts5 = str(int(time.time()))

step5_concat = str(key_tmp2).encode("utf-8") + id_c.encode("utf-8") + IP.encode("utf-8") + str(PORT).encode("utf-8") + ts5.encode("utf-8")
print("step5\n")
encryptor = PKCS1_OAEP.new(object_pk_s)
encrypted_step5 = encryptor.encrypt(step5_concat)
client_socket.send(encrypted_step5)

client_socket.send(encoded_key_2)
step6 = client_socket.recv(HEADER_LENGTH)
step6_decrypted = key_tmp2.decrypt(step6)
decoded_step6 = step6_decrypted.decode("utf-8")
print(decoded_step6)
print("decrypted step6:\n ")
print(step6_decrypted)

req = 'memo'


ts7 = str(int(time.time()))

step7 = req.encode("utf-8") + ts7.encode("utf-8")
key_session = "sesh key".encode("utf-8")
key_session = DesKey(key_session)
encrypted_step7 = key_session.encrypt(step7, padding=True)

client_socket.send(encrypted_step7)
step8 = client_socket.recv(HEADER_LENGTH)
print(step8)
client_socket.close()
# (ca_pub_key, ca_priv_key) = key.newkeys(256)


# CA = {'id_ca': 'ID_CA', 'pk_ca': pub_key, 'sk_ca': priv_key}


# user_input = input("Client: ") #asks for user input for identification
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #for streaming data
# client_socket.connect((IP, PORT)) #client program is the one to connect while server binds
# client_socket.setblocking(False) #sets blocking to
#
# user_id = user_input.encode("utf-8") #always has to translate to uit-8
# username_header = f"{len(user_id):<{HEADER_LENGTH}}".encode("utf-8")
# client_socket.send(username_header + user_id)
#
#
# encoded_request_ticket = request_ticket.encode("utf-8")
# print(encoded_request_ticket)
# message_header = f"{len(encoded_request_ticket) :< {HEADER_LENGTH}}".encode("utf-8")
# client_socket.send(message_header + encoded_request_ticket)

# ticket = client_socket.recv(1024)
# print(ticket)


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
# ticket_header = client_socket.recv(HEADER_LENGTH)
#
# ticket_length = int(ticket_header)
# #ticket_length = int(ticket_header.decode("utf-8").strip())
#
# ticket_message = client_socket.recv(ticket_length)
# print(ticket_message) #encrypted ticket
# decoded_ticket = key_c.decrypt(ticket_message, padding=True)
#
# # print(decoded_ticket.decode('utf-8').split("|")[3])
# encrypted_ticket_tgs = decoded_ticket.decode('utf-8').split("|")
# print("Received From Server Ticket-tgs" + "\n Shared Key: " + encrypted_ticket_tgs[0] + " \nID_tgs: " +  encrypted_ticket_tgs[1] + " \nTS2: "+ encrypted_ticket_tgs[2] + "\n Lifetime2: " + encrypted_ticket_tgs[3] + " \nTicket_tgs: " + encrypted_ticket_tgs[4] )
#
# authenticator = user_input
#
# string_step3 = idv + "|" + authenticator + "|"
#
# step3_send = string_step3.encode("utf-8") + encrypted_ticket_tgs[4].encode("utf-8")
# print(step3_send)
# step3_send_header = f"{len(step3_send) :< {HEADER_LENGTH}}".encode("utf-8")
# client_socket.send(step3_send_header + step3_send)
#
# # ticket_array = ticket_message.split("|")
# # print(ticket_array)
#
# # tgs_request_ticket = idv + "|" + ticket_array[3]
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