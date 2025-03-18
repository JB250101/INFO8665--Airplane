# Use Python base image
FROM python:3.10

# Set working directory in container
WORKDIR /INFO8665--AIRPLANE

# Copy requirements file
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Install Supervisor to manage multiple services
RUN apt-get update && apt-get install -y supervisor

# Copy app files into the container
COPY . .

# Copy the Supervisor configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose all required ports
EXPOSE 5000 5001 5002 5003 5004 5005 5006 8501

# Start Supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
