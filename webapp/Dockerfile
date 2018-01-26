FROM python:3.6.1-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Define mountable directories.
VOLUME ["/app"]

# Run app.py when the container launches
CMD ["python", "app.py"]
