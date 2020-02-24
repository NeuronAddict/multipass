FROM python:3

ENV PYTHONUNBUFFERED 1
ENV DOCKER_CONTAINER 1

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/

CMD '/code/docker/run.sh'
