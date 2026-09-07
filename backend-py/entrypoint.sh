#!/bin/bash
set -e

echo "Waiting for MySQL..."
# 循环等待 MySQL 就绪，最多等 30 秒
for i in $(seq 1 30); do
  if python -c "
import sqlalchemy
try:
    e = sqlalchemy.create_engine('$DATABASE_URL')
    e.connect()
    e.dispose()
except:
    exit(1)
" 2>/dev/null; then
    echo "MySQL is ready!"
    break
  fi
  if [ "$i" = "30" ]; then
    echo "ERROR: MySQL not reachable after 30s"
    exit 1
  fi
  echo "  retry $i/30..."
  sleep 1
done

echo "Running database migrations..."
alembic upgrade head

echo "Starting FastAPI server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
