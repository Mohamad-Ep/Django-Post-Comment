FROM python:3.11-slim

RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /srv/app
COPY ./core .

# Upgrade pip
RUN pip install --upgrade pip 

# Install Dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Allow Permissions
COPY entrypoint.sh .
RUN chmod +x ./entrypoint.sh