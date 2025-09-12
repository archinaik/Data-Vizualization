# Use official Python base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install required packages
RUN pip install --no-cache-dir pandas matplotlib requests

# Expose any ports if needed (optional)
# EXPOSE 8000

# Set default command to run your script
CMD ["python", "energy_app.py"]
