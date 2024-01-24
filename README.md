
# IZIPAY

Service for check bills


## Installation

#### 1. Install [Docker](https://www.docker.com)
#### 2. Create .env file at the root of the project

```bash
  DEBUG = 1 or 0
  SECRET_KEY = django random secret key
  DJANGO_ALLOWED_HOSTS = localhost 127.0.0.1 etc

  POSTGRES_HOST = postgres
  POSTGRES_PORT = 5432
  POSTGRES_DB = your db name
  POSTGRES_USER = your db user
  POSTGRES_PASSWORD = your db password

  REDIS_HOST = redis
  REDIS_PORT = 6379

  TRONGRID_APIKEY = your key
```
For create **django random secret key** you can use
```bash
  pip3 install django
  python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```
Also you can get **TRONGRID_APIKEY** at https://www.trongrid.io
## Run project

Start server
```bash
  docker-compose up
```

Create superuser
```bash
  docker-compose exec web python manage.py createsuperuser
```

After go to http://127.0.0.1/admin

Tests
```bash
  docker-compose exec web python manage.py test
```