# Use an official Python runtime as a base image
FROM python:2.7-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

RUN apt-get update

# RUN apt-get install python-mysqldb

RUN apt-get install -y gcc && apt-get install -y libmysqlclient-dev

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 8010

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]
