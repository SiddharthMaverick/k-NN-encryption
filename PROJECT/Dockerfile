# Use a pre-built SageMath Docker image as the base image
FROM python:3.10

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
# Set the working directory inside the container
WORKDIR /app
# Copy all Python scripts and other required files to the container
COPY QU.py cloud_server.py data_gen.py data_owner.py query_user.py database.txt DO.py /app/







# Install required Python packages
EXPOSE 9000
EXPOSE 17034

RUN pip install numpy
RUN pip install pandas
RUN pip install sagemath



# Since cloud server is inside container it's port is not exposed to other socket programs which are outside container.
# Hence we have to expose the port.
# Creates a non-root user with an explicit UID and adds permission to access the /app folder





# Run the cloud_server.py script when the container starts
CMD ["python3", "cloud_server.py"]
