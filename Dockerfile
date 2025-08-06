FROM python:3.12
WORKDIR /kudos

# Copy the current directory contents into the container at /app
COPY . /kudos

# Install the application dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .  

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable that a running container will use
ENV NAME=Kudos

# Setup an app user so the container doesn't run as the root user
RUN useradd app
USER app

CMD ["uvicorn", "kudos.main:app", "--host", "0.0.0.0", "--port", "8000"]