# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim

EXPOSE $PORT

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY ./requirements.txt ./
COPY ./Data/EQ_ANI_Watchdog.py ./
COPY ./Data/EQ_ANI_Transform.py ./
COPY ./Source ./

RUN python -m pip install -r requirements.txt

VOLUME /home/pwaver/Git/NCREE_LineBot/Data:./Data
CMD ["python3", "EQ_ANI_Watchdog.py", "--folder" "./Data"]