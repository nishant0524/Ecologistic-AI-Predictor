# 1. Use an official, lightweight Python runtime
FROM python:3.12-slim-bookworm

# 2. Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 3. Set the base working directory inside the container
WORKDIR /app

# 4. Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# 5. Copy the entire AINN_PROJECT folder into the container
COPY . /app/

# 6. Step inside the specific folder where manage.py lives
WORKDIR /app/carbon_project

# 7. Expose the port Django runs on
EXPOSE 8080

# 8. Start the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
