# LearnOps

A modular online learning platform built with FastAPI, designed with clean architecture principles and a clear migration path to microservices.

> **Status:** In active development — v1 covers core CRUD operations, authentication, and database relationships. WebSocket-based live classes and Kafka-based notifications are planned for future versions.

---

## What is LearnOps?

LearnOps is a backend platform for managing online and offline courses. Students can enroll in courses, submit homework, and track their grades. Teachers can create and manage courses, review submissions, and grade students. Admins oversee the platform — verifying teacher credentials, reviewing content, and handling refund requests.

---

## Architecture

The project follows **Modular Monolith** architecture with **Onion (Clean) Architecture** principles inside each module. This makes the codebase easy to reason about now, and straightforward to split into microservices later.

### Onion Layers (per module)

```
presentation/   →   FastAPI routers (HTTP layer)
application/    →   Business logic (services)
domain/         →   Core models and repository interfaces
infrastructure/ →   SQLAlchemy implementations, DB models
```

The key rule: **inner layers never depend on outer layers.** The business logic in `application/` doesn't know whether the database is PostgreSQL or an in-memory dict — it only talks to the abstract interface defined in `domain/`.

### Project Structure

```
learnops/
│
├── src/
│   ├── user/
│   │   ├── domain/
│   │   │   ├── models.py         # Pure Python dataclasses — no DB dependency
│   │   │   └── interfaces.py     # Abstract repository contracts
│   │   ├── application/
│   │   │   ├── user_service.py   # Registration, profile management
│   │   │   └── auth_service.py   # JWT creation and verification
│   │   ├── infrastructure/
│   │   │   ├── repository.py     # SQLAlchemy implementation
│   │   │   └── models.py         # ORM models
│   │   └── presentation/
│   │       ├── user_router.py
│   │       └── auth_router.py
│   │
│   ├── course/                   # Course creation, sessions, content
│   ├── enrollment/               # Enrollment, payments, refunds
│   ├── homework/                 # Submissions, grading, deadlines
│   └── admin/                   # User management, teacher verification
│
├── core/
│   ├── database.py               # Async SQLAlchemy setup
│   ├── dependencies.py           # Shared FastAPI dependencies (e.g. get_current_user)
│   └── exceptions.py             # Shared exception types
│
├── main.py
├── docker-compose.yml
└── README.md
```

---

## Features (v1)

### Students
- Register and authenticate (email/password or Google OAuth)
- Browse and search courses
- Enroll in courses (with payment flow)
- Submit homework (PDF/DOCX upload or multiple-choice)
- View grades and transcripts
- Rate courses and teachers after completion
- Request refunds

### Teachers
- Register and submit credentials for admin verification
- Create online and offline (package) courses
- Define sessions, upload materials and videos
- Set homework deadlines and grading criteria
- Review and grade student submissions
- Configure demo/free sessions

### Admins
- Verify teacher credentials
- Manage and ban users
- Review course ratings and flag inappropriate content
- Approve or reject refund requests
- Automated price validation for new courses (rule-based)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| ORM | SQLAlchemy (async) |
| Database | PostgreSQL |
| Authentication | JWT + OAuth2 |
| File Storage | (planned) S3-compatible |
| Containerization | Docker + Docker Compose |

---

## Roadmap

| Version | Focus |
|---|---|
| v1 (current) | Core CRUD, authentication, database relationships, initial frontend |
| v2 | WebSocket — live class sessions and real-time chat |
| v3 | Kafka — notifications and event-driven features |
| v4 | Split into microservices with API Gateway |

---

## Getting Started

```bash
git clone https://github.com/your-username/learnops.git
cd learnops

cp .env.example .env
docker-compose up --build
```

API docs available at `http://localhost:8000/docs`

---

## Design Decisions

**Why Modular Monolith first?**
Starting with microservices adds distributed systems complexity before the business logic is stable. A modular monolith lets us validate the domain model cheaply, then extract services along natural boundaries when the time is right.

**Why Onion Architecture?**
It keeps business logic framework-agnostic and easy to test. Services can be unit-tested with a fake in-memory repository — no database required.

**Why separate domain models from ORM models?**
SQLAlchemy models are an infrastructure detail. Keeping pure Python dataclasses in the domain layer means the core logic stays clean and portable.
