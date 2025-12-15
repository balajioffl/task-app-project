# Project

This project has a **Django backend** and a **React frontend**.

# folders

backend (django) and frontend (react)

# backend Setup

creating virtual environment

    python3 -m venv venv

    source venv/bin/activate 

# Install Django + MySQL client + DRF

    pip install django 

    pip install djangorestframework

    pip install mysqlclient 

    pip install django-cors-headers

# Create Django app

    python3 manage.py startapp app

# Install dependencies:

    pip install -r requirements.txt

# Configure MySQL in settings.py.

# Migrations

    python3 manage.py migrate

# Runserver

    python3 manage.py runserver

# frontend Setup

creating react app

    npx create-react-app frontend

start react server

    npm start
