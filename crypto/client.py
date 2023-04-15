import socket
from sympy import randprime
import Ass1_Functions as func

localIP = "127.0.0.1"
localPort = 20001
bufferSize = 1024
serverAddrPort = (localIP , localPort)
 
upper_limit = 32
lower_limit = 31#NOTE: min values are 8317,8353 which are 2**14 
              #so min lower_limit = 14
p = randprime(2**(lower_limit), 2**(upper_limit)) 
q = randprime(2**(lower_limit), 2**(upper_limit)) 
phi_n = (p-1)*(q-1)
e = randprime(1,phi_n) #3
n = p*q
#calculate private key (d)
d = pow(e,-1,phi_n)

# connecting to hosts
UDPClientSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM) 
 
# send public key (e) and n to second person
e_n = str(e)+'-'+str(p*q)
UDPClientSocket.sendto(str.encode(e_n), serverAddrPort) 

# get public key (e) and n from second person
e_n_2 = UDPClientSocket.recvfrom(bufferSize) 
e_n_2 = (e_n_2[0].decode()).split("-")
e2 = int(e_n_2[0])
n2 = int(e_n_2[1])

#record public keys in Channel_Information.txt to use it in the attack instead of listen to the socket 
# file1 = open("Channel_Information_1.txt","w")
# file1.write(str(n)+"\n")
# file1.write(str(e)+"\n")
# file1.close()
while(True):
    # user input
    chatText = input()    

    encrypted = func.encryption(chatText,n2,e2)
    # sending chat after encryption by encoding it
    encryptStrList = [str(x) for x in encrypted]
    
    msg_size = str.encode(str(len(encryptStrList)))
    UDPClientSocket.sendto(msg_size, serverAddrPort)
        
    for msgToSend in encryptStrList:
        bytesToSend1 = msgToSend
        # bytesToSend1 = "-".join(encryptStrList)
        bytesToSend1_encoded = str.encode(bytesToSend1)
        UDPClientSocket.sendto(bytesToSend1_encoded, serverAddrPort)
         
    
    # receiving status from server
    msgFromServerSize = UDPClientSocket.recvfrom(bufferSize) 
    decryptStrList = []
    for i in range(int(msgFromServerSize[0])):
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)
        decryptStrList.append(msgFromServer[0].decode())

    msgList = [int(i) for i in decryptStrList]
    msg = func.decryption(msgList,d,n)
    
    print("Other Person : "+msg)