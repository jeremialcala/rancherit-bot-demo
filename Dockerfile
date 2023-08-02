FROM python:3.11-slim

RUN mkdir /usr/src/app
WORKDIR /usr/src/app
RUN mkdir /usr/src/app/.aws

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY . ./

CMD ["gunicorn", "-b 0.0.0.0:8080", "app:app", "--log-file=-"]
EXPOSE 8080
