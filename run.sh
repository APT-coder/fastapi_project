#!/usr/bin/env bash
set -e
# load .env
if [ -f .env ]; then
export $(grep -v '^#' .env | xargs)
fi
# make sure DB exists (user should create DB manually or use psql)
# run alembic migrations
alembic upgrade head
# run uvicorn
uvicorn app.main:app --host ${APP_HOST:-0.0.0.0} --port ${APP_PORT:-8000} --reload