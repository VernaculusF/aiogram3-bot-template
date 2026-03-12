# aiogram3-bot-template

Advanced Telegram bot template on **aiogram 3** with:
- async PostgreSQL via SQLAlchemy
- finite state machine (FSM) for onboarding flow
- clean layered structure (config, db, services, handlers)
- Docker Compose for quick local launch

## Stack
- Python 3.11+
- aiogram 3
- SQLAlchemy 2 (async)
- asyncpg
- PostgreSQL 16

## Quick start

1. Copy environment file:
   ```bash
   cp .env.example .env
   ```
2. Set `BOT_TOKEN` in `.env`.
3. Run with Docker:
   ```bash
   docker compose up --build
   ```

## Local run (without Docker)

1. Create virtual environment and activate it.
2. Install package:
   ```bash
   pip install -e .
   ```
3. Ensure PostgreSQL is available with credentials from `.env`.
4. Start bot:
   ```bash
   python -m app.main
   ```

## Bot commands
- `/start` - welcome and trigger onboarding if user is new
- `/register` - start onboarding FSM manually
- `/profile` - show saved profile
- `/cancel` - cancel current FSM dialog

FSM onboarding flow stores: `full_name -> age -> city -> about`.

## Project structure

```text
app/
  main.py
  config.py
  db/
    base.py
    models.py
    session.py
    repo.py
  services/
    user_service.py
  bot/
    handlers/
      start.py
      profile.py
      registration.py
    middlewares/
      db.py
    states/
      registration.py
```

## Notes
- Tables are created automatically on startup for template convenience.
- For production, add migrations (Alembic), structured logging, and monitoring.
