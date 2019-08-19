FROM python:3.6-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

ADD requirements/production.txt /code/requirements/production.txt
ADD requirements/common.txt /code/requirements/common.txt
RUN pip install -r requirements/production.txt

ADD . /code/
ADD core/ /code/
RUN ./docker-services/nginx/install.sh
# Uncomment if using an Oracle database
# RUN ./docker-services/oracle/install.sh

ENTRYPOINT [ "/code/docker-services/runserver.sh" ]
