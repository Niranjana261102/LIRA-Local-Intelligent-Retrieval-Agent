# Use a lightweight Python version
FROM python:3.10-slim

# Set the working folder inside the container
WORKDIR /app

# Copy the requirements file first (to speed up installation)
COPY requirements.txt .

# Install dependencies
# We add --no-cache-dir to keep the image small
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the API when the container starts
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]