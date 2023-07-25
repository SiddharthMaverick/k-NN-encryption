import socket
import json

HOST = 'localhost'
DO_PORT = 5000
CS_PORT = 5071

n = int(input("Enter a positive integer: "))

# Send query to data owner
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as data_owner:
    data_owner.connect((HOST, DO_PORT))
    query = {"query": n}
    data_owner.sendall(json.dumps(query).encode())
    data = data_owner.recv(1024).decode()
    data = int(data)
    print(f"Data received from data owner: {data}")

# Send data to cloud server
    
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cloud_server:
    cloud_server.connect((HOST, CS_PORT))
    data = {"data": data}
    cloud_server.sendall(json.dumps(data).encode())
    result = cloud_server.recv(1024).decode()

    # Handle the case where the response is empty
    if result:
        try:
            result = json.loads(result)
            print(f"Result received from cloud server: {result}")
            prime_factors = result.get('result')
            if prime_factors:
                print(f"Prime factorization: {prime_factors}")
            else:
                print("No prime factors received.")
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
    else:
        print("Empty response received from the cloud server.")
