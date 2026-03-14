FROM python:3.11-slim
# Using a slim image to minimize container size and speed up deployments.

WORKDIR /app
# Setting the working directory inside the container.
# All subsequent commands will be executed relative to /app.

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Optimization: Copying requirements separately to leverage Docker layer caching.
# Re-installation only triggers if dependencies change, speeding up the build.

COPY . .
# Copying the rest of the source code after dependencies are installed.

EXPOSE 8000
# Documenting the port the app listens on. Actual mapping is done in docker-compose.yml.

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
# Launch command for FastAPI. 
# 0.0.0.0 allows the app to accept connections from outside the container.