#!/bin/bash
set -e

if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

echo "Waiting for PostgreSQL (user=$POSTGRES_USER, db=$DB_NAME)..."

until PGPASSWORD=$POSTGRES_PASSWORD psql \
  -h $DB_HOST \
  -U $POSTGRES_USER \
  -d $DB_NAME \
  2>&1;
  do echo "PostgreSQL is unavailable - sleeping..."
  sleep 2
done

echo "PostgreSQL is up! Running migrations..."
alembic -c telegram_bot/alembic.ini upgrade head
exec "$@"