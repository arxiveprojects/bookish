#!/bin/bash -ex
yum -y install python3 postgresql
# sudo yum -y install python3-pip

wget https://github.com/ikram9820/bookishpdf/archive/main.zip
unzip main.zip
cd  bookishpdf-main


pip3 install -r requirements.txt


export DJANGO_SETTINGS_MODULE='config.settings.prod'
export DJANGO_ALLOWED_HOSTS='*'
export SECRET_KEY=''
export PHOTOS_BUCKET=${SUB_PHOTOS_BUCKET}
export DATABASE_HOST=${SUB_DATABASE_HOST}
export DATABASE_USER=${SUB_DATABASE_USER}
export DATABASE_PASSWORD=${SUB_DATABASE_PASSWORD}
export DATABASE_DB_NAME=employees
cat database_create_tables.sql | \
mysql -h $$DATABASE_HOST -u $$DATABASE_USER -p$$DATABASE_PASSWORD


python3 manage.py makemigrations
python3 manage.py migrate
gunicorn -b 0.0.0.0:8000 config.wsgi