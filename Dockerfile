# Use Python 3.12 slim image as base
FROM python:3.12-slim

# Set environment variables to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

#installation of python , venv, pip module
RUN apt-get update && apt-get install -y python3 python3-venv python3-pip

# Install necessary dependencies for Chrome and Chromedriver
RUN apt-get update && apt-get install -y \
    wget \
    vim \
    curl \
    unzip \
    gnupg \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    libxtst6 \
    fonts-liberation \
    libappindicator3-1 \
    xdg-utils \
    --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Chromedriver
RUN CHROME_DRIVER_VERSION=$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
    wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip && \
    chmod +x /usr/local/bin/chromedriver

RUN google-chrome-stable --version

ARG USERNAME_REALTIMEDATA
ARG PASSWORD_REALTIMEDATA
ARG TOKEN

RUN echo 'USERNAME_REALTIMEDATA="${USERNAME_REALTIMEDATA}"' > .env && \
    echo 'PASSWORD_REALTIMEDATA="${PASSWORD_REALTIMEDATA}"' > .env && \
    echo 'TOKEN="${TOKEN}"' > .env

# #Install virtual env and activate 
RUN python3 -m venv .venv

# Switch to bash
SHELL ["/bin/bash", "-c"]

# Activate the virtual environment and install dependencies
RUN source .venv/bin/activate

# Copy requirements file to the working directory
COPY requirements.txt .

# Install dependencies and create a virtual environment
RUN .venv/bin/pip install --upgrade pip && \
    .venv/bin/pip install -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
#RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
#USER appuser

# Activate the virtual environment and define the entry point
CMD ["/bin/bash", "-c", "source .venv/bin/activate && python3 src/app.py"]