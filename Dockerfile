# Use the official Python 3.12.0 image as the base image
FROM python:3.12.0-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install additional spacy models
RUN python -m spacy download en_core_web_sm

# Copy the entire project into the container
COPY . .

# Set environment variables for Python
ENV PYTHONUNBUFFERED=1

# Define a volume for cache storage
VOLUME ["/app/cache"]

# Command to run the application
ENTRYPOINT ["python", "src/main.py"]
