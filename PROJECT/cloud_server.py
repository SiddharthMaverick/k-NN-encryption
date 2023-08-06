import random
import socket
import json
import numpy as np
from numpy import random
import gzip
import random
import time
import socket
import json
import numpy as np
import pickle


def receive_array(ji_socket):
    data = b""
    while True:
        packet = ji_socket.recv(10000)
        if not packet:
            break
        data += packet
        if len(packet) < 10000:
            break
    return pickle.loads(data)

def send_array(client_socket, data):
    serialized_data = pickle.dumps(data)
    client_socket.sendall(serialized_data)


def receive_data(client_socket):
    data = b""
    while True:
        packet = client_socket.recv(4096)
        if not packet:
            break
        data += packet

    # Decompress the received data
    decompressed_data = gzip.decompress(data)

    return pickle.loads(decompressed_data)

def send_large_data(socket, data):
    # Chunk size for data transmission
    chunk_size = 1024

    # Serialize and compress the data
    serialized_data = pickle.dumps(data)
    compressed_data = gzip.compress(serialized_data)

    # Send the data in chunks
    for i in range(0, len(compressed_data), chunk_size):
        socket.sendall(compressed_data[i:i + chunk_size])



#Function to compare distances

def knn(query, database, k=1):
    # Convert query to a NumPy array with float data type
    query_np = np.array(query, dtype=float)

    # Convert database to a NumPy array with float data type
    database_np = np.array(database, dtype=float)

    # Calculate the Euclidean distance between the query and each data point in the database
    distances = np.linalg.norm(database_np - query_np, axis=1)

    # Find the indices of the k-nearest neighbors
    knn_indices = np.argsort(distances)[:k]

    return knn_indices
    
def start_server():
    HOST = "0.0.0.0"
    CSPORT = 9000
    CS2PORT= 17034
    

    
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as CS_socket:
        CS_socket.bind((HOST, CSPORT))
        CS_socket.listen()

        print(f"Cloud Server is listening...on {HOST}:{CSPORT}")
        user_socket, user_address = CS_socket.accept()
        print(f"Connection from {user_address}")
        Database_Encrypted = receive_data(user_socket)
        print("Encrypted Database Collected from Data_Owner")
        print(Database_Encrypted)
            
        
        
    time.sleep(1)
    
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as CS2_socket:
        CS2_socket.bind((HOST, CS2PORT))
        CS2_socket.listen()
    
        print("Waiting for encrypted query from QU...")
        print(f"Cloud Server is listening...on {HOST}:{CS2PORT}")
        
        user_socket, user_address = CS2_socket.accept()
        print(f"Connection from {user_address}")
        
        
        data_bytes = user_socket.recv(1024)

        # Decode the received bytes and convert it back to a tuple
        data_string = data_bytes.decode('utf-8')
        data_tuple = tuple(data_string.split(','))
        
        print(f"Received tuple from server: {data_tuple}")
        
        
            

        print("Shape of Encrypted Database ",Database_Encrypted.shape)


        k=int(input("Enter the k -no. of nearest neighbours  : "))
        database_np=np.array(Database_Encrypted,dtype=float)
        query_np=np.array(data_tuple,dtype=float)
    
    
    
        TO_SEND_LIST=knn(database_np,query_np,k)
        print(TO_SEND_LIST)
        send_large_data(user_socket,TO_SEND_LIST)
    


if __name__ == "__main__":
    start_server()