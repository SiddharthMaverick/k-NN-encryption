# Project: K-nn Homomorphic Encryption 

This repository contains code and instructions for Project , where we deploy a cloud server inside a Docker container and connect to it to the data_owner and the query user running outside the container.

## Requirements

1. Python 3
2. DockerDesktop SHOULD BE THERE RUNNING 

## Repository Structure

The repository contains the following directories and files:

- `cloud_server.py/`: Contains the cloud server code and Dockerfile.
- `data_owner.py/`: Contains the data owner code.
- `query_user.py/`: Contains the query user code.
- `data_gen.py/`: Contains the code for database generation which is stored as database.txt
- `database.txt/`: Contains the database in form csv with 10000 points of 50 dimension and of range(-1000,1000)
- `Dockerfile/`: Contains docker code for running cloud_server.py as a container
- `README.md`: Instructions for setting up and running the project.

## Setup Instructions

Run the Cloud Server using docker commands in a Terminal(Ubuntu Linux Terminal as i have used) 
Then follow Data Owner Setup in separate Terminal and afterwards,
Use the instructions for Query User in separate Terminal.

Note:The Query User can give queries many times as the Data Owner is set listening until it stopped

Sequence should be 3->1->2->4

1. **Database Generation :**

   - Navigate to the `PROJECT` directory:
     ```
     cd /path/to/PROJECT
     ```
   - Run the data_gen.py using Python:
     ```
     python3 data_gen.py
     ```
   - Database generated in file database.txt
2. **Data Owner Setup:**

   - Navigate to the `PROJECT` directory:
     ```
     cd /path/to/PROJECT
     ```
   - Run the data owner server using Python:
     ```
     python3 data_owner.py
     ```
   - Enter the dimension of random vector u want in range (1-5):
     ```
       Enter positive integer c:
       Enter positive integer E:
     ```
   - Then Encryption of database in database.txt is done:
   - Then Encrypted database is printed
   - Now execute the query_user.py in separate terminal
   - Data Owner is listening for query_user to receive Encrypted query and Public key
   - Then after Receiving a Homomorphic database Aq it is sent to server.
   - Then Encrypted Database

3. **Cloud Server Setup:**

   - Navigate to the `PROJECT` directory:
     ```
     cd /path/to/PROJECT
     ```
   - Build the Docker image for the cloud server:
     ```
     docker build -t server .
     ```
   - Run the cloud server with ports 9000 and 17034 exposed
     ```
     docker run -it -p 9000:9000 -p 17034:17034 server
     ```
   - Proceed to execute data_owner.py
   - After getting both Encrypted Database and Encrypted query we set the value of k and give       a list back to user.
   - Note the k -value is not given by the user since it can harm the overall security of           database.

4. **Query User Setup:**

   - Navigate to the `PROJECT` directory:
     ```
     cd /path/to/PROJECT
     ```
   - Run the query user program using Python:
     ```
     python3 query_user.py
     ```
   - A random query is generated for ease of 50 dimension
     one can also use his query by initializing variable q in query_user.py
   - Query User  gets encrypted query and public key
   - Receives Aq(homomorphic encrypted query)
   - Then decrypted into a simpler query and sent to server to send list of k-nn
   - Proceed to cloud-server

## Dockerfile Execution Command

To build and run the cloud server container, use the following command:

```bash
docker build -t cloud-server 
docker run -it -p 9000:9000 -p 17034:17034 server

