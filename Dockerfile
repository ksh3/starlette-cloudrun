FROM python:3.7-slim-buster
LABEL maintainer "loFT LLC<info@loftllc.dev>"
LABEL author "Koushuu Matsubara<koushuu.matsubara@loftllc.dev>"

RUN pip install -U pip
RUN apt-get -y update && apt-get -y install npm gcc less && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /opt/app
COPY . /opt/app
WORKDIR /opt/app
RUN pip install pipenv
RUN pipenv install --system

EXPOSE 5000
CMD ["python", "main.py"]
