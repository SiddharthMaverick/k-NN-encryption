import socket
import json

HOST = 'localhost'
PORT = 5001

def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Cloud server listening on {HOST}:{PORT}...")
    while True:
        conn, addr = s.accept()
        with conn:
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break
                data = json.loads(data)
                print(f"Data received from query user: {data['data']}")
                factors = prime_factors(data['data'])
                response = {"result": factors}
                conn.sendall(json.dumps(response).encode())