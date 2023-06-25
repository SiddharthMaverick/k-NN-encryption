Assignment 4 - Deploying Cloud Server in a Container
This assignment focuses on deploying a cloud server in a Docker container and establishing communication between the query user, data owner, and the cloud server. The cloud server performs prime factorization on the query data and stores the results in a volume mount.

Setup Instructions
Clone or download this repository to your local machine.

Make sure you have Docker installed and running on your system.

Open a terminal or command prompt.

Navigate to the "Assignment4" folder.

Build the Docker image for the cloud server by running the following command:
docker build -t cloud-server ./CloudServer
Once the image is successfully built, create a Docker container based on the image, and map the necessary bind mount and volume mount. Run the following command: docker run -d -v /tmp/data:/app/data -v factors-db:/app/factors cloud-server

This command deploys the cloud server in a container and sets up the required mounts for query data and prime factorizations.

Adjust the IP address and port in the data owner and query user programs to connect to the cloud server running inside the container.

Run the data owner and query user programs outside the container to interact with the cloud server and perform the desired operations.
Run the data owner program to initiate the interaction with the cloud server.

Enter a positive integer when prompted by the data owner program.

The data owner program establishes a TCP connection with the cloud server and sends the input integer to the cloud server for processing.

The cloud server generates a random number, multiplies it with the received integer, and sends the product back to the data owner.

The data owner program closes the connection with the cloud server.

The data owner program establishes a TCP connection with the cloud server and sends the processed data to the cloud server.

The cloud server performs prime factorization on the received data and sends back the result to the data owner.

The data owner program closes the connection with the cloud server.

The data owner program displays the prime factorization result to the user via the terminal.

Repeat the above steps as needed for different integers.
