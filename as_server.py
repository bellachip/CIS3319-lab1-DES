import socket
import select
import des
from des import DesKey
import time
#server


HEADER_LENGTH = 1024
IP = "127.0.0.1" #dummy ipaddress"
PORT =1234 #dummy port
lifetime2 = 60
lifetime4 = 86400
adc = IP + ':' + str(PORT)
ts2 = str(int(time.time()))
pre_sharedkey_tgs = 'some key'
encoded_key_tgs = pre_sharedkey_tgs.encode()
key_tgs = DesKey(encoded_key_tgs)

pre_sharedkey_ctgs ='abcd eft'
encoded_key_ctgs = pre_sharedkey_ctgs.encode()
key_ctgs = DesKey(encoded_key_ctgs)

pre_sharedkey_c ='abcd efg'
encoded_key_c = pre_sharedkey_c.encode()
key_c = DesKey(encoded_key_c)






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
        return True



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

            #STEP 1
            client_auth = receive_message(client_socket) #receive requested ticket from client
            # client_auth.decode('utf-8')
            encoded = client_auth.get('data')
            decoded = encoded.decode('utf-8')
            request_ts_array = decoded.split("|") #array of idc, id_tgs, ts
            #recieves as decoded regular string
            idc = request_ts_array[0]
            id_tgs = request_ts_array[1]
            ts = request_ts_array[2]

            print("Received (1) C --> AS: " + "ID_c: " + idc + "ID_tgs: " + id_tgs + "TS1: " + ts)


            #STEP 2

            string_ticket = pre_sharedkey_tgs + idc + adc + id_tgs + ts2 + str(lifetime2)
            encoded_ticket = string_ticket.encode('utf-8')
            ticket_tgs = key_tgs.encrypt(encoded_ticket, padding=True)
            print(ticket_tgs)
            two_a = pre_sharedkey_ctgs + "|" + id_tgs + "|" + ts2 + "|" + str(lifetime2) + "|" + str(ticket_tgs)
            encoded_two_a = two_a.encode('utf-8')
            encrypted_tix = key_c.encrypt(encoded_two_a, padding=True)
            print(type(encrypted_tix))

            print('\n')
            message_header = f"{len(encrypted_tix) :< {HEADER_LENGTH}}".encode("utf-8")
            client_socket.send(message_header + encrypted_tix)
            # client_socket.send(id_tgs.encode('utf-8'))
            print('\n')

            step3_receive = receive_message(client_socket)

            encoded_step3_receive = step3_receive.get('data')
            decoded_step3_receive = encoded_step3_receive.decode('utf-8')
            decoded_step3_receive_array = decoded_step3_receive.split("|")
            encr = decoded_step3_receive_array[2]

            print(decoded_step3_receive_array[2].encode('utf-8'))

            #ab = f"{len(decoded_step3_receive_array[2]) :< {HEADER_LENGTH}}".encode("utf-8")

            # print(key_tgs.decrypt(decoded_step3_receive_array[2].encode('utf-8'), padding=True))

            # ticket_tgs = key_tgs.encrypt(encoded_ticket, padding= True

            # E_kc = str(key_tgs) + str(id_tgs) + str(ts2 )+ str(lifetime2) + str(ticket_tgs)
            # encrypted_E_kc = key_c.encrypt(E_kc, padding=True)
            # encoded_ticket = encrypted_E_kc.encode('utf-8')
            # encoded_E_kc = E_kc.encode('utf-8')







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
                    # client_socket.send('hello')
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
            for notified_socket in exception_sockets:
                sockets_list.remove(notified_socket)
                del clients[notified_socket]