# Dev manual

## Requirements

- [Python 3.11](https://www.python.org/downloads/)
- [Postresql](https://www.postgresql.org/download/)

## Setup

1. Setup
   ```sh
   git clone --recurse-submodules git@github.com:Pineapple217/Muze-Site.git
   ```
2. Create python virtual environment
   ```sh
   py -3.11 -m venv venv
   ```
3. Activate venv
   ```sh
   .\venv\Scripts\activate
   ```
4. Install python requirements
   ```sh
   pip install -r .\requirements.txt
   ```
5. Migrating database
   ```sh
   py .\django_app\manage.py migrate
   ```
6. Admin acount toevoegen
   ```sh
   py .\django_app\manage.py createsuperuser
   ```

## Run server

Server is beschikbaar op local netwerk, handig voor de mobiele versie te test.

```sh
py .\django_app\manage.py runserver 0.0.0.0:8000
```

## Aanpassing aan de databank maken

Migrations maken:

```sh
py .\django_app\manage.py makemigrations
```

Migrations toe passen:

```sh
py .\django_app\manage.py migrate
```

## Vertalingen

Vertalingen ophalen uit de code.
Het resualtaat hier van kan terug gevonden worden in `./locale/nl/django.po`

Zorg dat je in de `./django_app` dir zit.

```sh
django-admin makemessages -l nl
```

Eens de vertalingen in het `.po` bestand zijn ingevuld moeten ze compiled woorden zodat django ze kan gebruiken.

```sh
django-admin compilemessages
```
