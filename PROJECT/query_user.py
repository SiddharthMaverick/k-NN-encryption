import socket
import pickle
import numpy as np
import random
from math import gcd
from sage.all import *
import random
import numpy as np
import socket
import json
from decimal import *
import gzip
import time


    

class paillier:
    
    def __init__(self):
        c=1
        while c==1:
            p1=random_prime(2**5,True,2**4)
            p2=random_prime(2**5,True,2**4)
            if p1!=p2 and gcd(p1*p2,(p1-1)*(p2-1)):
                break
        #self.func = lambda x : (x-1)//n
        n=int(p1*p2)
        self.n=n
        self.lam=int(lcm(p1-1,p2-1))
        #a=(mod(g**self.lam,n**2))
        a=0
        self.a=a
        while True :
            g=int(random.randint(1,n**2-1))
            self.g=g
            L=pow(g,self.lam,n**2)
            self.a=(int(L)-1)//self.n
            if gcd(self.a,n)==1 and gcd(self.g,n)==1 :
                break
        self.u=int(inverse_mod(self.a,n))
    
    def get_public_key(self):
        self.pubk=(self.n,self.g)
        return self.pubk
    
    #Encryption func
    def encrypt(self,m):
        
            r=random.randint(1,self.n-1)
            cipher1=pow(self.g,m,self.n**2)
            cipher2=pow(r,self.n,self.n**2)
            cipher=cipher1*cipher2
            
            return cipher
    #Decryption func
    def decrypt(self,cipher):
        
        t=pow(cipher,self.lam,self.n**2)
        k=(int(t)-1)//int(self.n)
        m=mod(k*self.u,self.n)
        
        return m


def receive_array(server_socket):
    data = b""
    while True:
        packet = server_socket.recv(4096)
        if not packet:
            break
        data += packet
        if len(packet) < 4096:
            break
    return pickle.loads(data)

def receive_data(client_socket):
    data = b""
    while True:
        packet = client_socket.recv(1024)
        if not packet:
            break
        data += packet

    # Decompress the received data
    decompressed_data = gzip.decompress(data)

    return pickle.loads(decompressed_data)


def send_array(server_socket, data):
    serialized_data = pickle.dumps(data)
    server_socket.sendall(serialized_data)

def send_large_data(socket, data):
    # Chunk size for data transmission
    chunk_size = 1024

    # Serialize and compress the data
    serialized_data = pickle.dumps(data)
    compressed_data = gzip.compress(serialized_data)

    # Send the data in chunks
    for i in range(0, len(compressed_data), chunk_size):
        socket.sendall(compressed_data[i:i + chunk_size])



def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost',8000 ))
    
        
    d=50
    o=paillier()
    pubk=o.get_public_key() #(I)QU generates a public key pair {pk, sk} of homomorphic cryptosystem
    print(pubk[0])

    #q is the query
    q=np.random.randint(low=-1000,high=1001,size=(d))
    
    print(q)
    ciph=np.random.randint(low=-100,high=101,size=(d))
    for i in range(d):
        m=int(q[i])
        cipher=o.encrypt(m)
        ciph[i]=cipher
    
    
    print(ciph)

    # Send the matrix to the server
    send_array(client_socket, ciph)
    
    ack=client_socket.recv(1024)
    
    print(pubk)
    if ack.decode()=="ACK":
        client_socket.send((str(pubk)).encode())
    
    
    received_Aq = receive_array(client_socket)

    print("Received Aq : ")
    print(received_Aq)

    print("Decrypt Aq : ")
    
    pt=[]
    for i in range(len(received_Aq)):
        m=int(received_Aq[i])
        ptext=o.decrypt(m)
        if(ptext>1000):
            ptext=int(ptext)
            ptext-=pubk[0]
        pt.append(ptext)


    print(pt)

    client_socket.close()
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as QU_socket:
        QU_socket.bind(('localhost', 18000))
        QU_socket.listen(1)


        print("Query User is listening for confirmation from data_owner")
        while True:
            user_socket, user_address = QU_socket.accept()
            print(f"Connection from {user_address}")
            ack=user_socket.recv(1024)

            print(pt)
            if ack.decode()=="ACK":
                print("Affirmative Proceed!")
            break
        
    QU_socket.close()
    print("Query User sending Encrypted Query to Server")
    a=int(input("Enter 1 to proceed"))
    
    QU_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    QU_socket1.connect(('localhost',17034))
    time.sleep(1)
    print("Sending query....")
    print(pt)
    data_string = ",".join(map(str, pt))
    data_bytes = data_string.encode('utf-8')

    # Send the bytes object to the client
    QU_socket1.send(data_bytes)
    print("Receiving list ....")
    RP=receive_data(QU_socket1)
        
    print("KNN LIST :   ",RP)
    

    
if __name__ == "__main__":
    start_client()
