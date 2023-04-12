# Deploy

```env
DEPLOY=True
DEBUG=False

SECRET_KEY=
DISCORD_WEBHOOK_URL=

EMAIL_HOST=
EMAIL_PORT=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

DJANGO_LOGLEVEL=info
DJANGO_ALLOWED_HOSTS=

DB_USER=
DB_PASSWD=
DB_HOST=postgres-db
DB_PORT=5432
DB_NAME=
```

## Secret key

Onderstaande code kan gebruikt worden voor een key te generen die dan aan de .env kan toegevoegd worden.

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

# Dev

```env
DEPLOY=False

DISCORD_WEBHOOK_URL=

EMAIL_HOST=
EMAIL_PORT=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

DJANGO_LOGLEVEL=info

DB_USER=
DB_PASSWD=
DB_HOST=localhost
DB_PORT=5432
DB_NAME=
```
