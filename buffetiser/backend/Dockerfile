# Use the official Python image
FROM python:3.13-slim

# Set environment variables
# Send output to console
ENV PYTHONUNBUFFERED 1

ENV LANG en_AU.UTF-8

# Create and set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY wait-for-it.sh /usr/local/bin/wait-for-it.sh
RUN chmod +x /usr/local/bin/wait-for-it.sh

# Copy the entire backend code into the container
COPY . /app/

# Expose the Django port (default is 8000)
EXPOSE 8000

# Run migrations and start the app using Gunicorn
# CMD ["gunicorn", "buffetiser_api.wsgi:application", "--bind", "0.0.0.0:8000"]
