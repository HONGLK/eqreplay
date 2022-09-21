# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim

EXPOSE $PORT

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY ./requirements.txt ./
COPY ./Data/Watchdog.py ./
COPY ./Data/Transform.py ./
COPY ./Source ./Source

RUN pip install --trusted-host -r requirements.txt


CMD ["python3", "Watchdog.py"]