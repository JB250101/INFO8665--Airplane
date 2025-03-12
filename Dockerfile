# Use Python base image
FROM python:3.10

# Set working directory in container
WORKDIR /app

# Copy requirements file
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files into the container
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Define environment variables (optional)
# ENV FLASK_APP=main.py
# ENV FLASK_RUN_HOST=0.0.0.0

# Command to run the application
CMD ["python", "dev/training_services.py"]
