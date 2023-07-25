# Assignment 4: Cloud Server with Docker

This repository contains code and instructions for Assignment 4, where we deploy a cloud server inside a Docker container and connect to it from the query user running outside the container.

## Requirements

1. Python 3
2. DockerDesktop SHOULD BE THERE RUNNING 

## Repository Structure

The repository contains the following directories and files:

- `cloud_server/`: Contains the cloud server code and Dockerfile.
- `data_owner/`: Contains the data owner code.
- `query_user/`: Contains the query user code.
- `README.md`: Instructions for setting up and running the project.

## Setup Instructions

Run the Cloud Server using docker commands in a Terminal(Ubuntu Linux Terminal as i have used) 
Then follow Data Owner Setup in separate Terminal and afterwards,
Use the instructions for Query User in separate Terminal.

Note:The Query User can give queries many times as the Data Owner is set listening until it stopped

Sequence should be 2->1->3

1. **Data Owner Setup:**

   - Navigate to the `data_owner` directory:
     ```
     cd /path/to/Assignment4/data_owner
     ```
   - Run the data owner server using Python:
     ```
     python3 data_owner.py
     ```

2. **Cloud Server Setup:**

   - Navigate to the `cloud_server` directory:
     ```
     cd /path/to/Assignment4/cloud_server
     ```
   - Build the Docker image for the cloud server:
     ```
     docker build -t cloud-server .
     ```
   - Run the cloud server container with bind mount and volume mount:
     ```
     docker run -p 5001:5001 -v /tmp/data:/app/data -v factors-db:/app/factors-db cloud-server
     ```

3. **Query User Setup:**

   - Navigate to the `query_user` directory:
     ```
     cd /path/to/Assignment4/query_user
     ```
   - Run the query user program using Python:
     ```
     python3 user.py
     ```
   - Enter a positive integer when prompted, and the program will communicate with the data owner server and the cloud server (inside the Docker container) to perform the prime factorization. The results will be displayed on the terminal.

## Dockerfile Execution Command

To build and run the cloud server container, use the following command:

```bash
docker build -t cloud-server ./cloud_server
docker run -p 5001:5001 -v /tmp/data:/app/data -v factors-db:/app/factors-db cloud-server

