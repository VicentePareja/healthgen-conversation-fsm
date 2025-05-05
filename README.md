# Healthgen Scheduler

A minimal, Dockerized full-stack boilerplate for a healthcare scheduler chatbot.

## 🚀 Overview

This project demonstrates a three-tier application using Docker Compose:

1. **Backend**: FastAPI server with PostgreSQL, SQLAlchemy ORM, and Alembic migrations.
2. **Database**: PostgreSQL container seeded with initial data.
3. **Frontend**: Next.js (TSX) chatbot prototype served by Nginx or run locally for development.

## ✅ Features

* **API Endpoints**

  * `GET /hello` – Returns a greeting message.
  * `GET /items` – Returns seeded records from the database.
* **Chatbot UI (TSX)**

  * Simple mock FSM logic responding to user inputs.
  * Interactive message options and auto-scrolling.

## 🛠️ Tech Stack

| Tier          | Technology                                                                 |
| ------------- | -------------------------------------------------------------------------- |
| Backend       | Python · FastAPI · Uvicorn · SQLAlchemy · Alembic                          |
| Database      | PostgreSQL                                                                 |
| Frontend      | Next.js (App Router) · React · TypeScript (TSX) · lucide-react · shadcn/ui |
| Orchestration | Docker · Docker Compose                                                    |

## 📁 Repository Structure

```
project-root/
├── .env                   # Environment variables
├── docker-compose.yml     # Service orchestration
├── db/
│   └── init.sql           # Database seed script
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── alembic.ini
│   ├── alembic/
│   │   └── versions/
│   └── app/
│       ├── main.py        # FastAPI application
│       ├── database.py    # SQLAlchemy setup
│       ├── models.py      # ORM models
│       ├── crud.py        # Data access logic
│       └── schemas.py     # Pydantic schemas
└── frontend/
    ├── Dockerfile
    ├── package.json
    ├── tsconfig.json      # TypeScript configuration
    ├── next.config.js
    ├── public/            # Static assets
    ├── app/
    │   ├── layout.tsx     # Root layout
    │   └── page.tsx       # Chatbot page component
    ├── components/
    │   └── ui/            # Button.tsx, Input.tsx, Card.tsx
    └── lib/
        └── utils.ts       # Utility functions (e.g., `cn`)
```

## ⚙️ Prerequisites

* Docker >= 20.10
* Docker Compose >= 1.29
* Node.js & npm (for local frontend dev)

## 📥 Getting Started

1. **Clone the repo**

   ```bash
   git clone <repo-url>.git
   cd project-root
   ```

2. **Configure environment**

   In `.env` and adjust values if needed:

   ```ini
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=healthgen
   DB_PORT=15432

   DATABASE_URL=postgresql://postgres:postgres@db:5432/healthgen
   API_PORT=8000
   WEB_PORT=3000
   ```

3. **Build and start services**

   ```bash
   docker-compose up --build
   ```

   * The `db` service will run the seed script on first launch.

## 🔍 Verifying Setup

* **Chatbot UI**

  Open your browser at [http://localhost:3000](http://localhost:3000) to see the TSX-based chatbot UI.

## 📈 Next Steps

* Integrate chatbot UI with FastAPI-backed FSM endpoints.
* Add user authentication and session management.
* Expand database schema and migrations.
* Implement end-to-end tests (pytest & Jest).

## 📜 License

MIT © Healthgen, Inc.
