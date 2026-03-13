# aiogram3-bot-template

Advanced Telegram bot template on **aiogram 3** with:
- async PostgreSQL via SQLAlchemy
- finite state machine (FSM) for onboarding flow
- profile update flow via repeated registration
- clean layered structure (config, db, services, handlers)
- Docker Compose for quick local launch

## Stack
- Python 3.11+
- aiogram 3
- SQLAlchemy 2 (async)
- asyncpg
- PostgreSQL 16
- Alembic
- APScheduler

## Quick start

1. Copy environment file:
   ```bash
   cp .env.example .env
   ```
2. Set `BOT_TOKEN` in `.env`.
3. Start PostgreSQL:
  ```bash
  docker compose up -d postgres
  ```
4. Apply migrations:
  ```bash
  docker compose run --rm bot alembic upgrade head
  ```
5. Run bot:
   ```bash
  docker compose up --build -d bot
  ```
6. Check logs:
  ```bash
  docker compose logs -f bot
   ```

## Local run (without Docker)

1. Create virtual environment and activate it.
2. Install package:
   ```bash
   pip install -e .
   ```
3. Install development tools (optional):
  ```bash
  pip install -e .[dev]
  ```
4. Ensure PostgreSQL is available with credentials from `.env`.
5. Apply migrations:
  ```bash
  alembic upgrade head
  ```
6. Start bot:
   ```bash
   python -m app.main
   ```

## Test

```bash
pytest -q
```

## Scheduler

Template includes APScheduler-based periodic task.
By default it sends report to `BOT_ADMINS` with current registered users count.

Environment variables:
- `SCHEDULER_ENABLED=true|false`
- `SCHEDULER_REPORT_INTERVAL_MINUTES=60`

## Bot commands
- `/start` - welcome and trigger onboarding if user is new
- `/register` - start onboarding FSM manually (creates or updates profile)
- `/profile` - show saved profile
- `/cancel` - cancel current FSM dialog
- `/admin` - show admin command list
- `/stats` - admin-only users statistics
- `/report_now` - admin-only immediate report to all admins

FSM onboarding flow stores: `full_name -> age -> city -> about`.

If user already exists, `/register` updates existing profile fields.

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
- Schema is managed by Alembic migrations.
- If `alembic upgrade head` fails with `relation "users" already exists`, use the current migration file from this template and rerun the command.
- For production, add structured logging, monitoring, and CI checks.
