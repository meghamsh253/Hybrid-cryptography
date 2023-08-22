from Crypto.Cipher import Blowfish
from AesEverywhere import aes256
from Crypto import Random
from struct import pack
from azure.storage.blob import BlobServiceClient
import os
import multiprocessing as mp
from multiprocessing import Manager

#azure blob details
storage_account_key = "jSkNXJGRboB8zdqc5Ar0T5MltBYY8JqdDoTqiLEDBHpnEDO9FcV9xjIDzcbR3QKfP9SE8nY0ohw/+ASt3ql6KQ=="
storage_account_name = "demo012"
connection_string = "DefaultEndpointsProtocol=https;AccountName=demo012;AccountKey=jSkNXJGRboB8zdqc5Ar0T5MltBYY8JqdDoTqiLEDBHpnEDO9FcV9xjIDzcbR3QKfP9SE8nY0ohw/+ASt3ql6KQ==;EndpointSuffix=core.windows.net"
container_name = "file"

f = open("C:/Users/meghamsh/Desktop/file.txt",'r')
#input file path
g=f.read()      
f.close()
def encrypt1(l1,key): 
    msg1=g[int(len(g)//2):]
    encrypted = aes256.encrypt(msg1,key)
    l1[0]=encrypted.hex()   
    
def encrypt2(l1,key):
    a=g[:int(len(g)//2)]
    key= bytes(key,'utf-8')
    iv = Random.new().read(8)
    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    plaintext=bytes(a,'utf-8')
    plen = 8 - divmod(len(plaintext),8)[1]
    padding = pack('b'*plen, *([plen]*plen))
    msg1 = iv + cipher.encrypt(plaintext + padding)
    l1[1]=msg1.hex()
 
    _main__":    
    with Manager() as manager:
        l1 = manager.dict()
        key=str(input('Enter your key'))
        p2=mp.Process(target=encrypt2,args=[l1,key,]) 
        p1=mp.Process(target=encrypt1,args=[l1,key,]) 
        p1.start()
        p2.start()
        p1.join()
        p2.join()
        x= str(len(l1[0])).rjust(10,"0")+l1[0]+l1[1]   
        file = open('encryptedfile.txt','w')
        file.write((x))   
        file.close()  
        print('Output saved to file')        
        print('Uploading file to cloud')

      #uploading into Azure blob
        file_path=os.path.join(os.getcwd(),'encryptedfile.txt')
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob='encryptedfile.txt')
        with open(file_path,'rb') as data:
            blob_client.upload_blob(data)
            #print(f".Uploaded {file_name}.”)
            print(' Uploading completed')
               
         
