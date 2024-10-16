# Step 1: Use an official Python runtime as a parent image
FROM python:3.12-slim

# Step 2: Set the working directory
WORKDIR /app

# Step 3: Copy the current directory contents into the container at /app
COPY . .

# Step 4: Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Make port 80 available to the world outside this container
EXPOSE 80

# Step 6: Define environment variable
# ENV TELEGRAM_BOT_TOKEN=""

# Step 7: Run app.py when the container launches
CMD ["python", "main.py"]

