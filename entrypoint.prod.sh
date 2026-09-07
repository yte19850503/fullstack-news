#!/bin/bash
set -e

cd /app/backend-py

echo "Waiting for MySQL..."
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

echo "Seeding default admin user..."
python -c "
from app.database import SessionLocal, engine
from app.models.user import User, Role
from app.core.security import hash_password
from sqlalchemy import inspect

if not inspect(engine).has_table('users'):
    print('Users table does not exist yet, skipping seed')
else:
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.email == 'admin@news.com').first()
        if not admin:
            admin = User(
                email='admin@news.com',
                password=hash_password('Admin123!'),
                name='管理员',
                role=Role.ADMIN,
            )
            db.add(admin)
            db.commit()
            print('Default admin user created: admin@news.com / Admin123!')
        else:
            print('Admin user already exists')
    finally:
        db.close()
"

echo "Checking static dist directories..."
ls -la /app/admin/dist/ 2>&1 || echo "WARNING: /app/admin/dist not found"
ls -la /app/frontend/dist/ 2>&1 || echo "WARNING: /app/frontend/dist not found"

echo "Starting FastAPI server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
