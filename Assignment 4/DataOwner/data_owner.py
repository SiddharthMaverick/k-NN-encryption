import socket
import json
import random

def data_owner():
   
    data_owner_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_owner_socket.bind(("localhost", 5001))
    data_owner_socket.listen(1)

    print("Data Owner is ready and listening for connections...")

    while True:
       
        client_socket, address = data_owner_socket.accept()
        print("Data Owner received a connection from:", address)

       
        query = json.loads(client_socket.recv(1024).decode())
        num = query["query"]
        print("Data Owner received query:", num)

      
        random_num = random.randint(1, 10000)
        product = num * random_num
        print("Data Owner calculated product:", product)

       
        response = {"data": product}
        client_socket.send(json.dumps(response).encode())

       
        client_socket.close()
        print("Data Owner closed the connection with the query user\n")

if __name__ == "__main__":
    data_owner()
