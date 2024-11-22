# Use the official Python image from the Docker Hub
FROM python:3.11.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt /app/.

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Run app.py when the container launches
CMD ["gunicorn", "main:app", "--worker-class", "gevent", "--bind", "0.0.0.0:8001"]
