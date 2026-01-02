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


# Task Management Backend (Django + DRF + Celery + Redis)

This project is a backend Task Management system built using **Django** and **Django Rest Framework** with **JWT Authentication**, **Redis caching**, and **Celery** for background task processing.

It supports:
- Role-based access (Admin / User)
- Task CRUD operations
- Search & Pagination
- Redis caching
- Asynchronous task logging using Celery

---

## Features

- JWT Authentication (Login & Protected APIs)
- Admin & User role handling
- Create, Update, Delete Tasks
- Search & Pagination
- Redis caching for task list APIs
- Celery background tasks for activity logging
- MySQL database
- File upload support


##  Tech Stack

- **Backend**: Django, Django REST Framework  
- **Auth**: JWT (SimpleJWT)  
- **Database**: MySQL  
- **Cache & Broker**: Redis  
- **Async Tasks**: Celery  
- **Frontend**: React



