# Use the official Python image as the base image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the application files into the working directory
COPY . /app

# Install the application dependencies
# Change the pip install command to use the --no-cache-dir flag to avoid caching the installation files
RUN pip install --no-cache-dir -r requirements.txt

# Define the entry point for the container
# Change the CMD to provide the argument '0.0.0.0:8000' instead of '127.0.0.1:8000' to allow access from outside the container
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]

# Expose the port 8000
EXPOSE 8080
