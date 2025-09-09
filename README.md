# Smart Bank — Minimal Banking App (Backend + Simple Frontend)

This is a **production-ready starter** for a banking-style application named **Smart Bank**.
It includes:

- FastAPI backend (JWT auth, users, accounts, transfers, transactions).
- SQLite by default (easily switch to Postgres by changing `DATABASE_URL`).
- Simple vanilla JS frontend for login, viewing accounts, and making transfers.

> ⚠️ This is a demo/starter. For real money, integrate with regulated payment rails and perform full KYC/AML, audit trails, and security hardening.

## Quick Start (Backend)

1. **Create a virtual environment** (Python 3.11+ recommended):

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure environment**:

```bash
cp .env.example .env
# Edit .env and set a strong SECRET_KEY
```

3. **Run dev server**:

```bash
uvicorn app.main:app --reload
```

4. **Docs**:
- OpenAPI docs: http://127.0.0.1:8000/docs

## Simple Frontend

Open `smartbank-frontend/index.html` in a local server (e.g. VS Code Live Server) and set API base URL at the top of `app.js` if needed.

## Features

- Sign up, login (JWT)
- Create account (checking/savings), list accounts
- Internal transfers between accounts (atomic)
- Transaction history with descriptions
- Basic idempotency via client-supplied key for transfers (optional header)
- CORS enabled for local dev

## Security Notes

- Passwords hashed with bcrypt (passlib).
- Access tokens (JWT) with HMAC SHA256—**rotate** and secure `SECRET_KEY`.
- SQLAlchemy ORM with transactions for money movement.
- Server-side validation on amounts and ownership.
- Includes very simple rate-limit stubs you can expand.

## Switch to Postgres

- Set `DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/smartbank`
- Add dependency `psycopg2-binary` to `requirements.txt`.

## Disclaimer

This code is provided **as-is** for educational/demo purposes and is **not** a complete banking core. You are responsible for compliance, security, and regulatory requirements in your jurisdiction.
