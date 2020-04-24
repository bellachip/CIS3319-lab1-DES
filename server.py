import socket
import select
import des
from des import DesKey
import time
#server
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
import binascii
from Crypto.Hash import SHA256
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5

from rsa import key, common, encrypt

HEADER_LENGTH = 5000
IP = "127.0.0.1" #dummy ipaddress"
PORT =1234 #dummy port
id_s = 'ID-Server'
ts1 = str(int(time.time()))
id_c = 'ID-Client'


#S registers with the certificate authroity CA to obtain its own public/private keys and certificate
# the message is encrypted with CA's public key such thatt only CA can decrypt the message
#The message includes a temporary DES key Ktmpl for CAA to ecrypt the response message/
#This is necessary because the response contains the private key for S, which is very sensitive.




#
# message = (key_tmp1 + id_s + ts2).encode("urf-8")
# crypto = encrypt(message, pub_key) #ecrypted tempraroy key + ids + ts1

# message_header = f"{len(crypto) :< {HEADER_LENGTH}}".encode("utf-8")
# client_socket.send(message_header + crypto)


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creating socket
server_socket.bind((IP, PORT)) #server program binds with the right ip and port
server_socket.listen() #listend
print("waiting for CA connection...")
conn_ca, address = server_socket.accept()
print("connection established with CA ")

f = open("file.txt", "rb")
ca_public_key = f.read()

object_ca_pk = RSA.import_key(ca_public_key) #object



temp_key ='some key'
encoded_key_c = temp_key.encode()
key_tmp1 = DesKey(encoded_key_c) #key_temp1

#STEP1

s1_str = str(key_tmp1) + "|" + id_s + "|" + ts1
encoded_s1_str = s1_str.encode("utf-8")
# RSA_encrypted = object_ca_pk.encrypt(s1_str, 32)

encryptor = PKCS1_OAEP.new(object_ca_pk)
encrypted = encryptor.encrypt(s1_str.encode("utf-8"))

print(encrypted)

# print(RSA_encrypted)
conn_ca.send(encrypted)

step2 = conn_ca.recv(HEADER_LENGTH)
cert_s = conn_ca.recv(HEADER_LENGTH)
pk_s = conn_ca.recv(HEADER_LENGTH)
decrypted_step2 = key_tmp1.decrypt(step2)
decrypted_cert_s = key_tmp1.decrypt(cert_s)
# decrypted_pk_s = key_tmp1.decrypt(pk_s)
object_pk_s = RSA.import_key(pk_s) #object
print(decrypted_step2)
print(cert_s)



conn_ca.close()


print("waiting for client connection...")
conn_c, address2 = server_socket.accept()
print("connection established with client")

step3 = conn_c.recv(HEADER_LENGTH)

ts4 = str(int(time.time()))
step4 = pk_s + decrypted_cert_s + ts4.encode("utf-8")

conn_c.send(step4)

conn_c.send(pk_s)
step5 = conn_c.recv(HEADER_LENGTH)
print(step5)




session_key ='sesh key'
encoded_session_key = session_key.encode()
session_key_step6 = DesKey(encoded_session_key) #key_temp1

lifetime_session = 86400
ts6 = str(int(time.time()))
step6 = encoded_session_key + str(lifetime_session).encode("utf-8") + id_c.encode("utf-8")+ ts6.encode("utf-8")

key_tmp2 = conn_c.recv(HEADER_LENGTH)

object_key_tmp2 = DesKey(key_tmp2) #key_temp1

encrypted_step6 = object_key_tmp2.encrypt(step6, padding=True)
#
conn_c.send(encrypted_step6)

step7 = conn_c.recv(HEADER_LENGTH)

data = 'take cis3319 class this afternoon'
ts8 = str(int(time.time()))

step8 = data.encode("utf-8") + ts8.encode("utf-8")
encrypted_step8 = session_key_step6.encrypt(step8, padding=True)

conn_c.send(encrypted_step8)







