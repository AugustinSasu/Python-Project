# Use official Python image
FROM python:3.11-slim

# Set working directory in the container
# This is where the app code will be copied
# and where commands will be run
WORKDIR /math-service

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#added for sqlite3 support
RUN apt update && apt install -y sqlite3
# Copy app code
COPY . .

ENV PYTHONPATH=/math-service


# Expose FastAPI default port
EXPOSE 8000

# Start app
# main:app refers to the FastAPI app instance in main.py
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
