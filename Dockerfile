# Use a Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the port your Flask app will run on
EXPOSE 5000

# Set environment variables (if needed)
ENV PORT 5000

# Run the Flask application
CMD ["python", "app.py"]