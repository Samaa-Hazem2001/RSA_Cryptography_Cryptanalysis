import math
import Ass1_Functions as func
import decimal

def attack(plainText,cipherText,e,n):
    sqrt_decimal_n = decimal.Decimal(n).sqrt()
    for num in range(1, int(sqrt_decimal_n) + 1):
    # all prime numbers are greater than 1
        if(n%num == 0):
            p=num
            q=int (n/num)
    
    phi_n = (p-1)*(q-1)
    d = pow(e,-1,phi_n)

    decryptStrList = cipherText
    cipherList = [int(i) for i in decryptStrList]
    attacked_plainText = func.decryption(cipherList,d,n)
    
    #to deal with extra spaces at the end of recovered plainText ,we use "strip()"
    if (attacked_plainText.strip() == plainText.strip()):
        print("HACKED!!!")
    return 

