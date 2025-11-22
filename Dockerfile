# Stage 1: Build Stage - Use a lightweight Python base image
FROM python:3.11-slim AS builder

# Set environment variables for the application
ENV PYTHONUNBUFFERED 1
ENV APP_HOME /app

# Create the application directory
WORKDIR $APP_HOME

# Install dependencies
# Copy only the requirements file first to take advantage of Docker's layer caching
COPY requirements.txt .

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final Image - Use an even smaller base for the final runtime
FROM python:3.11-slim

# Set the environment variable for where the application lives
ENV APP_HOME /app
WORKDIR $APP_HOME

# Copy installed dependencies and application files from the builder stage
# This keeps the final image clean and small (security and efficiency)
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy the entire agent application and evaluation structure
# Note: You copy the entire structure, as the final agent might run evaluation internally.
COPY agent_app/ ./agent_app/
COPY evaluation/ ./evaluation/

# Define the entry point for the container
# When the container starts, it runs the 'main.py' file to start the agent service.
# For a live service, this would typically start a server (e.g., FastAPI) wrapper around the agent.
CMD ["python", "agent_app/main.py"]
