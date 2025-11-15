# my_fastapi_project


- Use PostgreSQL local DB. Configure `DATABASE_URL` in `.env`.
- Create DB first: `createdb my_fastapi_db` (or use pgAdmin)
- Install deps: `python -m pip install -r requirements.txt`
- Initialize alembic (already included). Run migrations: `alembic upgrade head` or use `./run.sh`.
- Start server: `./run.sh` or `uvicorn app.main:app --reload`