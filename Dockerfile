FROM python:3.10-alpine

WORKDIR /app

# installeert alle pip pakages
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy alle files van het Django project
COPY ./django_app /app

WORKDIR /app

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]