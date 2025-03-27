## Getting Started

Setup project environment with python -m venv myenv.

```bash
$ git clone https://github.com/ikram9820/bookishpdf.git
$ cd bookishpdf
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt

$ python manage.py makemigrations books
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```

## Production Setup with Docker

```bash
$ docker-compose build
$ docker-compose up -d
$ docker-compose exec web python manage.py migrate
$ docker-compose exec web python manage.py collectstatic
```

## Development Setup
```bash
$ docker-compose -f docker-compose.dev.yml up
```

## Home Page

![Default Home View](./screenshot/home.png?raw=true "Home ss")

## Detail Page

![Detail Page View](./screenshot/detail.png?raw=true "detail ss")
