
# Use a Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies with timeout
RUN pip install --no-cache-dir --timeout 100 -r requirements.txt

# Copy the data folder
COPY data/ data/

# Copy the application code into the container
COPY . .

# Expose the port your Flask app will run on
EXPOSE 4000

# Set environment variables (if needed)
ENV PORT=4000

# Run the Flask application with Gunicorn
CMD ["gunicorn", "wsgi:app", "-b", "0.0.0.0:4000"]