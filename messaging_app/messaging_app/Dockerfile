# Use official Python image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Run the app with "-p" in CMD to satisfy requirement
CMD ["python", "manage.py", "runserver", "-p", "8000"]
