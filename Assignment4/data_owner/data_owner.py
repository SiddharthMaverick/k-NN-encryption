import socket
import json
import random

HOST = 'localhost'
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Data owner listening on {HOST}:{PORT}...")
    while True:
        conn, addr = s.accept()
        with conn:
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break
                query = json.loads(data)
                print(f"Query received from query user: {query['query']}")
                rand_num = random.randint(1, 10000)
                product = query['query'] * rand_num
                conn.sendall(str(product).encode())
