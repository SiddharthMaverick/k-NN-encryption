# Use a Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the cloud.py file into the container
COPY cloud.py /app/cloud.py
#This are prerequisite
# Install required Python dependencies
RUN pip install json5

# Define a mount point for the query data on the host machine
VOLUME /tmp/data

# Create a volume named factors-db for storing prime factorisations
VOLUME factors-db:/app/factors-db

# Set environment variables
ENV HOST=0.0.0.0
ENV PORT=5071
#Although I have exposed the below 2 but only is used I have kept to avoid confusion
# Expose the port on which the cloud server will listen
EXPOSE 5071
EXPOSE 5000

#using python3 command instead of python
# Command to start the cloud server when the container is launched
CMD ["python3", "cloud.py"]
