#!/bin/sh
set -e  # Exit on any error

HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8283}"

# Wait for database to be ready
echo "Waiting for database to be ready..."
sleep 5

# Attempt database migration
echo "Attempting to migrate database..."
poetry run alembic upgrade head || {
    echo "ERROR: Database migration failed!"
    echo "Please check your database connection and try again."
    echo "If the problem persists, check the logs for more details."
    exit 1
}
echo "Database migration completed successfully."

# Start the server
CMD="poetry run letta server --host $HOST --port $PORT"
if [ "${SECURE:-false}" = "true" ]; then
    CMD="$CMD --secure"
fi

echo "Starting Letta server at http://$HOST:$PORT..."
echo "Executing: $CMD"
exec $CMD
