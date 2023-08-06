
import numpy as np
import pandas as pd
import socket
import pickle
import ast
import random
from sage.all import *
import sys
from decimal import *
from numpy import random
import gzip
import time




def pi_inverse(j,pi):
    for i in range(len(pi)):
        if(pi[i]==j):
            return i

def p_encrypt(a,b,c):
    n=int(a)
    g=int(b)
    m=c
    r=random.randint(n-1)
    cipher1=pow(int(g),int(m),int(n)**2)
    cipher2=pow(int(r),int(n),int(n)**2)
    cipher=cipher1*cipher2
    return cipher

def receive_array(client_socket):
    data = b""
    while True:
        packet = client_socket.recv(4096)
        if not packet:
            break
        data += packet
        if len(packet) < 4096:
            break
    return pickle.loads(data)

def send_array(ji_socket, data):
    serialized_data = pickle.dumps(data)
    ji_socket.sendall(serialized_data)


def send_large_data(socket, data):
    # Chunk size for data transmission
    chunk_size = 4096

    # Serialize and compress the data
    serialized_data = pickle.dumps(data)
    compressed_data = gzip.compress(serialized_data)

    # Send the data in chunks
    for i in range(0, len(compressed_data), chunk_size):
        socket.sendall(compressed_data[i:i + chunk_size])


def A_form(pi,M,q_encrypted,pubk,d,c,epsilon):
    eta=d+c+epsilon+1
    beta_q=Decimal(random.randint(1000))
    R_q=random.randint(1001,size=c)
    Aq=np.zeros(eta)
    for i in range(eta):
        Aq[i]=(p_encrypt(pubk[0],pubk[1],0))
        for j in range(eta):
            t=(pi_inverse(j,pi))
            if(t<d):
                phi=int(beta_q*int(M[i,j]))
                # if(phi>0):
                Aq[i]=Aq[i]*pow(int(q_encrypted[t]),int(phi),pubk[0]**2)
                # else:
                #     A_q[i]=A_q[i]/(int(q_encrypted[t])**abs(int(phi)))

            elif(t==d):
                phi=int(beta_q*int(M[i,j]))
                Aq[i]=(Aq[i]*p_encrypt(pubk[0],pubk[1],phi))
            elif(t<=d+c):
                omega=t-d-1
                phi=(beta_q*int(M[i,j])*int(R_q[omega]))
                Aq[i]=(Aq[i]*int(p_encrypt(pubk[0],pubk[1],phi)))
    return Aq




def start_data_owner():
    d=50
    m=10000

    c=int(input("Enter positive integer c  : "))
    E=int(input("Enter another postive integer E  : "))
    eta=d+c+E+1
    while True:
        # Generate a random nxn matrix with float values between low and high
        M = np.random.uniform(1,20 , size=(eta, eta))
        M=np.round(M,decimals=0)

        # Check if the matrix is invertible (non-singular)
        if np.linalg.det(M) != 0:
            break
    S=np.random.uniform(1000,1100,size=d+1)
    tau=np.random.uniform(100,111,size=c)

    arr=np.arange(1,eta+1)
    Pi=np.random.default_rng(seed=42)

    Key={"Matrix":M,"S":S,"T":tau,"Pi":Pi}

    D_encrypted=np.empty((0,eta))


    #permutation array
    pi_list=np.arange(eta)
    Pi.shuffle(pi_list)

    M_inv=np.linalg.inv(M)

    cf=pd.read_csv("database.txt",header=None)


    data = pd.read_csv('database.txt', header=None)

    # Step 2: Initialize an empty list to store the new vectors p'
    new_prime = []

    for i in range(len(data)):
        Vi=np.random.uniform(4,26,size=E)
        p = data.loc[i].values
        p_i=np.append(p,0)
        p_prime_new = S - 2*p_i
        p_prime_new[-1]=p_prime_new[-1]+(np.linalg.norm(p_i))**2
        p_prime_new=np.append(p_prime_new,tau)
        p_prime_new=np.append(p_prime_new,Vi)
        Pi.shuffle(p_prime_new)
        p_dash=np.dot(p_prime_new,M_inv)
        new_prime.append(p_dash)

    print(new_prime)
    # Step 3: Create the matrix D' by stacking the new vectors p'
    D_encrypted = np.vstack(new_prime)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as DO_socket:
        DO_socket.bind(('localhost', 8000))
        DO_socket.listen(1)

        print("Data Owner is listening...")
        while True:
            user_socket, user_address = DO_socket.accept()
            print(f"Connection from {user_address}")

            # Receive the matrix from the client
            received_Encrypted_query = receive_array(user_socket)
            print("Received Encrypted Query:")
            print(received_Encrypted_query)
        
            Pi.shuffle(received_Encrypted_query)
        
        
            if len(received_Encrypted_query)!=d:
                print("Query not d-dimensional re-enter query")
                sys.exit()
        
            user_socket.send("ACK".encode())
        
            data=user_socket.recv(1024)
            if data:
                pubk=data.decode()
            
                print("Public key received : ",pubk)
        
        
            numbers_tuple = ast.literal_eval(pubk)
            
        
        
            Aq=A_form(pi_list,M,received_Encrypted_query,numbers_tuple,d,c,E)
        

            print("Sending Aq to Query User ......")
            print(Aq)
            send_array(user_socket, Aq)
                    
        
            user_socket.close()
        
        
            break
    
    
    print("Encrypted Database Sending to Server.....")
    print(D_encrypted)
    
    time.sleep(10)

    
    #with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    #   client_socket.connect(('localhost', 9000))

    
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("WORKS")
    server_socket.connect(('localhost',9000))
    print("THIS ")
    send_large_data(server_socket, D_encrypted)
    server_socket.close()
    time.sleep(10)
    print("Acknowledging Data Owner to Query USER.....")
    
    user_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    user_socket1.connect(('localhost',18000))
    user_socket1.send("ACK".encode())
    user_socket1.close()
    
        
    
if __name__ == "__main__":
    start_data_owner()







