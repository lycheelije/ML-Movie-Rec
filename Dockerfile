# pull official base image
FROM python:3.9.5-slim-buster

# set work directory
WORKDIR /project
COPY . /project

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt