FROM python:3.8-slim-buster

RUN mkdir pimpositor

COPY . pimpositor

WORKDIR pimpositor

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["waitress-serve", "--port=5053","--call", "flaskr:create_app"]

