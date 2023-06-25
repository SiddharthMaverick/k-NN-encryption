import socket
import json


def get_prime_factors(num):
    factors = []
    divisor = 2

    while divisor <= num:
        if num % divisor == 0:
            factors.append(divisor)
            num = num / divisor
        else:
            divisor += 1

    return factors


def cloud_server():
    # Create a socket to listen for connections
    cloud_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cloud_server_socket.bind(("localhost", 5000))
    cloud_server_socket.listen(1)

    print("Cloud Server is ready and listening for connections...")

    while True:
        # Accept incoming connection
        client_socket, address = cloud_server_socket.accept()
        print("Cloud Server received a connection from:", address)

        # Receive data from the query user
        data = json.loads(client_socket.recv(1024).decode())
        product = data["data"]
        print("Cloud Server received data:", product)

        # Calculate the prime factorization of the product
        prime_factors = get_prime_factors(product)
        result = {"result": prime_factors}

        # Send the result back to the query user
        client_socket.send(json.dumps(result).encode())

        # Close the connection with the query user
        client_socket.close()
        print("Cloud Server closed the connection with the query user\n")


if __name__ == "__main__":
    cloud_server()
