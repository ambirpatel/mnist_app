FROM python:3.8-slim-buster

WORKDIR /source

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY source ./source

CMD [ "python3", "./source/app.py"]