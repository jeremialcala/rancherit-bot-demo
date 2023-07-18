FROM python:3.6.10-slim-buster

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . ./

CMD ["gunicorn", "-b 0.0.0.0:8080", "app:app", "--log-file=-"]
EXPOSE 8080
