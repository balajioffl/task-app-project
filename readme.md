#  Task Management Platform

A full-stack **SaaS-based Task Management Platform** built as part of the **Build SaaS Based Product series**. This project demonstrates real-world backend architecture, frontend integration, scalability, security, and deployment practices using **Django, Django REST Framework, React, Redis, Celery, and Docker**.

---

##  Project Highlights

- Modular SaaS-ready backend architecture
- JWT-based authentication & authorization
- Role-Based Access Control (RBAC)
- Scalable task management APIs
- Caching, background jobs, and real-time updates
- Production-ready deployment & CI/CD

---

## Tech Stack

### Backend

- Django
- Django REST Framework (DRF)
- drf-spectacular (Swagger / OpenAPI)
- SimpleJWT (Authentication)
- PostgreSQL / SQLite (Dev)
- Redis (Caching & Celery broker)
- Celery (Background jobs)
- Django Channels (WebSockets)

### Frontend

- React
- React Router (Protected routes)
- Axios

### DevOps

- Docker & Docker Compose
- CI/CD Pipeline
- Cloud Deployment


## Feature Breakdown

### Project Initialization & Setup

- Django project & app structure
- Environment-based settings
- `.env` configuration

### Core Backend Models & Migrations

- Custom User model
- Task model
- Role & Permission models

### JWT Authentication

- Login / Logout APIs
- Access & Refresh tokens

### Role-Based Access Control (RBAC)

- Admin / Manager / User roles
- Permission-based APIs
- RBAC rework for scalability

### React Auth UI & Protected Routes

- Login & Register
- Auth context
- Protected routes

### Task Management

- Backend CRUD APIs
- Frontend CRUD integration

### Global Error Handling & Validation

- Centralized error responses
- Login validation rework

### File Uploads & Media Handling

- Profile images
- Media configuration

### Pagination & Search

- Page-based pagination
- Search & dropdown-based page size

### Redis Caching

- Cached task list APIs
- Cache invalidation

### Background Jobs with Celery

- Async email notifications
- Long-running tasks

### Advanced Features

- Multi-column search & filters
- CSV & PDF export
- Notifications (Email + Celery)
- Real-time updates (WebSockets)

---

##  Testing
```bash
python3 manage.py test
```

---

##  Docker
```bash
docker-compose up --build
```

---

##  API Documentation
- Swagger UI: `/api/docs/swagger/`
- ReDoc UI: `/api/docs/redoc/`
- OpenAPI Schema: `/api/schema/`

---

##  Deployment
- Gunicorn
- Environment variables
- Static & media handling

---

##  Local Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver
```

```bash
npm install
npm start
```
