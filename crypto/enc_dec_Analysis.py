import time
from sympy import randprime
import matplotlib.pyplot as plt 
import Ass1_Functions as func
import chatAttack 

encryptionTime = []
decryptionTime = []
keySize = []
# loop for different n size in bits for analysis
for bits in range(28,3000):
    print("bits",bits) 
    p = randprime(2**(bits//2), 2**(bits//2+1)) 
    q = randprime(2**(bits//2), 2**(bits//2+1)) 
    phi_n = (p-1)*(q-1)
    e = randprime(1,phi_n) 
    n = p*q
    #calculate private key (d)
    d = pow(e,-1,phi_n)
    keySize.append(len(format(n, 'b')))
    plainText = "samaa"
    
    start_enc = time.time()
    cipherText = func.encryption(plainText,n,e)
    end_enc = time.time()
    encryptionTime.append(end_enc - start_enc)
    
    start_dec = time.time()
    msg = func.decryption(cipherText,d,n)
    end_dec = time.time()
    decryptionTime.append(end_dec - start_dec)

plt.title('Encryption Time Analysis')     
plt.plot(keySize,encryptionTime, color ='tab:blue') 
plt.xlabel('Key Size')
plt.ylabel('Time')
plt.show()

plt.title('Decryption Time Analysis')     
plt.plot(keySize,decryptionTime, color ='tab:blue') 
plt.xlabel('Key Size')
plt.ylabel('Time')
plt.show()

# print("encryptionTime",encryptionTime)
# print("decryptionTime",decryptionTime)
# print("keySize",keySize)

