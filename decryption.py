from Crypto.Cipher import Blowfish
from AesEverywhere import aes256
import multiprocessing as mp
import time
from multiprocessing import Manager


f = open("D:/first/encryptedfile678.txt",'r')
#insert file path here

st=f.read()
value=int(st[:15])
e1=st[15:value+15]
e2=st[value+15:]    

def decrypt2(l2):
    key = b'helloworld'
    bs = Blowfish.block_size
    ciphertext=bytes.fromhex(e2)
    iv = ciphertext[:bs]
    ciphertext = ciphertext[bs:]
    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    msg1 = cipher.decrypt(ciphertext)
    last_byte = msg1[-1]
    msg1 = msg1[:- (last_byte if type(last_byte) is int else (last_byte))]
    l2.append(msg1.decode())
    
   
def decrypt1(l1):  

    msg2=bytes.fromhex(e1)
    sol=aes256.decrypt(msg2,'helloworld')
    l1.append(sol.decode())

if __name__=="__main__":

    with Manager() as manager:
        l1 = manager.list()
        l2 = manager.list()
        p2=mp.Process(target=decrypt2,args=[l1,]) 
        p1=mp.Process(target=decrypt1,args=[l2,]) 
        p1.start()
        p2.start()
        p1.join()
        p2.join()
        g=l1[0]+l2[0]
    file = open('decryptedfile147.txt','w')
    file.write((g))   
    file.close()   
