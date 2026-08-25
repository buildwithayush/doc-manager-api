# Doc Manager API

A backend API for managing user documents, built with FastAPI.

## Tech Stack

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* Alembic
* Docker

## Project Structure

```text
app/
├── api/
│   └── v1/
│       ├── endpoints/
│       │   └── health.py
│       └── router.py
├── core/
├── db/
└── main.py

tests/
.env.example
.gitignore
README.md
requirements.txt
```

## Getting Started

### Clone the repository

```bash
git clone <https://github.com/buildwithayush/doc-manager-api.git>
cd doc-manager-api
```

### Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**Windows**

```bash
.venv\Scripts\activate
```

**Linux/macOS**

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file using `.env.example`:

```bash
cp .env.example .env
```

Then configure the required environment variables.

### Run the application

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

### Health Check

```text
GET /api/v1/health
```
