# Use a base image that supports Python 3.11
FROM python:3.11-slim

WORKDIR /app

# Copy the files into the container
COPY poetry.lock pyproject.toml /app/

# Install Poetry and dependencies
RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev

# Copy the rest of the application code
COPY . .

# Copy the templates folder
COPY templates /app/templates

ENV MODEL_SERVICE_URL=http://127.0.0.1:8080

# Set the command to run the Flask app
CMD ["python", "app.py"]
