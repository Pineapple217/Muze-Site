FROM python:3

WORKDIR /app

# installeert alle pip pakages
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy alle files van het Django project
COPY . . 

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]