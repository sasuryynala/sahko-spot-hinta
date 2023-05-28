# Use the official Python image as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the Python script into the container
COPY main.py /app/main.py

# Install the required dependencies
RUN pip install requests pytz

# Set the entry point for the container
CMD ["python", "main.py"]