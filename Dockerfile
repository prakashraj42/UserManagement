# Use an official Python runtime as base image
FROM python:3.12

# Set the working directory
WORKDIR /UserManagement

# Copy requirements and install dependencies
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt


RUN pip install uvicorn fastapi

# Copy the application code
COPY . .

# Expose the FastAPI port
EXPOSE 8000

# Start FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
