# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.12-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

ARG USERNAME_REALTIMEDATA
ARG PASSWORD_REALTIMEDATA
ARG TOKEN

RUN echo "USERNAME_REALTIMEDATA=${USERNAME_REALTIMEDATA}" > .env && \
    echo "PASSWORD_REALTIMEDATA=${PASSWORD_REALTIMEDATA}" > .env && \
    echo "TOKEN=${TOKEN}" > .env

#Install virtual env and activate 
RUN python -m venv .venv && \
    source .venv/bin/activate

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
#RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
#USER appuser

# Expose a port (if the app listens on one)
#EXPOSE 8000

# Define the command to run the application
CMD ["python", "src/app.py"]
