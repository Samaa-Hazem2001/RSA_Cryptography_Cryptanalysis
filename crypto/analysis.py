import time
from sympy import randprime
import matplotlib.pyplot as plt 
import Ass1_Functions as func
import chatAttack 

attackTime = []
keySize = []
# loop for different n size in bits for analysis
for bits in range(28,63):

    print("bits",bits)
    p = randprime(2**(bits//2), 2**(bits//2+1)) 
    q = randprime(2**(bits//2), 2**(bits//2+1)) 
    phi_n = (p-1)*(q-1)
    e = randprime(1,phi_n) 
    n = p*q
    #calculate private key (d)
    d = pow(e,-1,phi_n)
    keySize.append(len(format(n, 'b')))
    
    plainText = "samaa speaking" 
    cipherText = func.encryption(plainText,n,e)
    
    start_attack = time.time()
    msg = chatAttack.attack(plainText,cipherText,e,n)
    end_attack = time.time()
    attackTime.append(end_attack - start_attack)

plt.title('Attack Time Analysis')     
plt.plot(keySize,attackTime, color ='tab:blue') 
plt.xlabel('Key Size')
plt.ylabel('Time')
plt.show()

# print("attackTime",attackTime)
# print("keySize",keySize)
