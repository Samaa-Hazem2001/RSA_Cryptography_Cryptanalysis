import math 

############################   encryption   ############################

def CharToNum(plainText):
    pText_list = list(plainText)
    cNumValue_list = [] #
    for i in range(len(pText_list)):
        #print(pText_list[i])
        charASCII = ord(pText_list[i])
        #if it is characters
        if charASCII > 96 and charASCII < 123 :
            cNumValue_list.append(charASCII - 87)
        #if its a number 0->9
        elif charASCII > 47 and charASCII < 58 :
            cNumValue_list.append(charASCII - 48)
        else:
            cNumValue_list.append(36)
    return cNumValue_list

def CharGrouping(cNumValue_list):
    spaces = [36]
    numCharPerGroup = 5
    mod_result = len(cNumValue_list)%numCharPerGroup
    increased_spaces =[]
    if(mod_result !=0):
        increased_spaces = (numCharPerGroup-(mod_result))*spaces
    cNumValue_list = cNumValue_list+increased_spaces
    #NOTE: integer division in python is done by // not /
    numGroups = len(cNumValue_list)//numCharPerGroup
    groupValues = []
    for i in range(numGroups):
        groupValue = 0
        for j in range(numCharPerGroup):
            groupValue += cNumValue_list[5*i+j]* ((37)**(4-j))
        groupValues.append(groupValue)
    return groupValues


def RSA_encryption(groupValues,n,e):
    encryptValues = []
    for i in range(len(groupValues)):
        encryptValues.append(pow(groupValues[i],e,n))
    return encryptValues

def encryption(plainText,n,e):
    cNumValue_list = CharToNum(plainText)
    groupValues = CharGrouping(cNumValue_list)
    cipherText = RSA_encryption(groupValues,n,e)
    return cipherText

############################   decryption   ############################
def exctractCharLists(cText_arr):
    numCharPerGroup = 5
    allCharLists = []
    for i in range(len(cText_arr)):
        groupI = cText_arr[i]
        charList =[]
        first4Char = 0
        for j in range(numCharPerGroup-1):
            groupI_1 = groupI%(37**(4-j))
            charValue = (groupI - groupI_1) // ((37**(4-j)))
            charList.append(charValue)
            groupI = groupI_1
        charList.append(groupI)
        allCharLists.append(charList)

    return allCharLists

def recoverChar(allCharLists):
    strings = ""
    for i in range(len(allCharLists)):
        for j in range(len(allCharLists[0])):
            req_char = allCharLists[i][j]
            if  req_char==  36 :
                strings +=' '
            elif req_char > 9:
                strings +=chr(req_char + 87 )
            else:
                strings +=chr(req_char + 48 )
    return strings

def RSA_decryption(cipherText,d,n):
    decryptValues = []
    for i in range(len(cipherText)):
        decryptValues.append(pow(cipherText[i],d,n))
    return decryptValues

def decryption(cipherText,d,n):
    cText_arr = RSA_decryption(cipherText,d,n)
    allCharLists = exctractCharLists(cText_arr)
    plainText = recoverChar(allCharLists)
    return plainText
