import socket
from sympy import randprime
import Ass1_Functions as func

localIP = "127.0.0.1"
localPort = 20001
bufferSize = 1024

upper_limit = 32
lower_limit = 31 #NOTE: min values are 8317,8353 which are 2**14 
              #so min lower_limit = 14
p = randprime(2**(lower_limit), 2**(upper_limit)) 
q = randprime(2**(lower_limit), 2**(upper_limit)) 

phi_n = (p-1)*(q-1)
e = randprime(1,phi_n) #3
n = p*q
#calculate private key (d)
d = pow(e,-1,phi_n)

UDPServerSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))

# get public key (e) and n from second person
e_n_2, addr1 = UDPServerSocket.recvfrom(bufferSize)
e_n_2 = (e_n_2.decode()).split("-")
e2 = int(e_n_2[0])
n2 = int(e_n_2[1])

# send public key (e) and n to second person
e_n = str(e)+'-'+str(p*q)
UDPServerSocket.sendto(str.encode(e_n), addr1)

#record public keys in Channel_Information.txt to use it in the attack instead of listen to the socket 
# file1 = open("Channel_Information_2.txt","w")
# file1.write(str(n)+"\n")
# file1.write(str(e)+"\n")
# file1.close()
while(True):
    chatText = input()  
    # receiving name from client
    msgReceivedSize, addr1 = UDPServerSocket.recvfrom(bufferSize)

    decryptStrList = []
    for i in range(int(msgReceivedSize)):
        msgReceived, addr1 = UDPServerSocket.recvfrom(bufferSize)
        decryptStrList.append(msgReceived.decode()) 
        
    msgList = [int(i) for i in decryptStrList]
    msgReceived = func.decryption(msgList,d,n)
    print("Other Person : "+msgReceived)

    encrypted = func.encryption(chatText,n2,e2)
    # sending encoded status of name and pwd
    encryptStrList = [str(x) for x in encrypted]
    
    msg_size = str.encode(str(len(encryptStrList)))
    UDPServerSocket.sendto(msg_size, addr1)
       
    for msgToSend in encryptStrList:
        bytesToSend1 = msgToSend
        bytesToSend1_encoded = str.encode(bytesToSend1)
        UDPServerSocket.sendto(bytesToSend1_encoded, addr1)
