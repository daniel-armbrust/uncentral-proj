# Use a base image with Python
FROM python:3.9-slim

# Install Tkinter and other dependencies
RUN apt-get update \
    && apt-get install -y python3-tk git sqlite3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && git clone https://github.com/daniel-armbrust/uncentral-proj.git


# Set the working directory
WORKDIR /uncentral-proj/uncentral

# Copy your Tkinter application code into the container

# Command to run your Tkinter application
CMD ["python", "uncentral.py"]
