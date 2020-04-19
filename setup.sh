#!/bin/sh

pip install -r requirements.txt

# Prompts the user to create an admin account
python manage.py createsuperuser

# Perform initial migration and populate database with sample data
python manage.py migrate
python manage.py populate_data

# Starts the server on 127.0.0.1:8000
python manage.py runserver