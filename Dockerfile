FROM python:3.8-slim-bullseye

# Install build dependencies
RUN apt-get update && apt-get install -y make gcc --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir pimpositor

COPY . pimpositor

WORKDIR pimpositor

# Upgrade pip and install requirements
RUN pip install --upgrade pip && pip install -r requirements.txt

# Set environment variables for Flask
ENV FLASK_APP=flaskr

CMD ["waitress-serve", "--port=5053","--call", "flaskr:create_app"]
