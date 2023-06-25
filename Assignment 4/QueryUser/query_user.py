import socket
import json

def query_user():
   
    num = int(input("Enter a positive integer: "))

   
    data_owner_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_owner_socket.connect(("localhost", 5001))

    
    query = {"query": num}
    data_owner_socket.send(json.dumps(query).encode())

    
    product = data_owner_socket.recv(1024).decode()

    
    data_owner_socket.close()


    cloud_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cloud_server_socket.connect(("localhost", 5000))

   
    data = {"data": product}
    cloud_server_socket.send(json.dumps(data).encode())

    # Receive the result from the cloud server
    response = json.loads(cloud_server_socket.recv(1024).decode())

    # Close the connection with the cloud server
    cloud_server_socket.close()

    # Print the prime factors received from the cloud server
    print("Prime Factors:", response["result"])

if __name__ == "__main__":
    query_user()
