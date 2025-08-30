#!/bin/bash
set -e

# Entrypoint script for Django application
# This script handles initialization tasks before starting the main application

echo "🚀 Starting Sistema Produtos - Version: ${APP_VERSION:-unknown}"

# Function to wait for database
wait_for_db() {
    echo "⏳ Waiting for database to be ready..."
    
    # Extract database connection details from environment
    DB_HOST=${DB_HOST:-localhost}
    DB_PORT=${DB_PORT:-5432}
    DB_NAME=${DB_NAME:-sistema_produtos}
    
    # Wait for database to be ready
    until nc -z "$DB_HOST" "$DB_PORT"; do
        echo "Database is unavailable - sleeping"
        sleep 1
    done
    
    echo "✅ Database is ready!"
}

# Function to wait for Redis
wait_for_redis() {
    if [ -n "$REDIS_URL" ]; then
        echo "⏳ Waiting for Redis to be ready..."
        
        REDIS_HOST=${REDIS_HOST:-localhost}
        REDIS_PORT=${REDIS_PORT:-6379}
        
        until nc -z "$REDIS_HOST" "$REDIS_PORT"; do
            echo "Redis is unavailable - sleeping"
            sleep 1
        done
        
        echo "✅ Redis is ready!"
    fi
}

# Function to run database migrations
run_migrations() {
    echo "🗄️ Running database migrations..."
    python manage.py migrate --noinput
    echo "✅ Migrations completed!"
}

# Function to collect static files
collect_static() {
    echo "📦 Collecting static files..."
    python manage.py collectstatic --noinput
    echo "✅ Static files collected!"
}

# Function to create cache table
create_cache_table() {
    echo "🗃️ Creating cache table..."
    python manage.py createcachetable || echo "⚠️ Cache table already exists or not configured"
}

# Function to validate Django setup
validate_django() {
    echo "🔍 Validating Django configuration..."
    python manage.py check --deploy
    echo "✅ Django validation passed!"
}

# Main execution logic
main() {
    case "$1" in
        "web")
            echo "🌐 Starting web server..."
            wait_for_db
            wait_for_redis
            
            # Only run migrations and collect static if SKIP_INIT is not set
            if [ -z "$SKIP_INIT" ]; then
                run_migrations
                collect_static
                create_cache_table
            fi
            
            validate_django
            
            echo "🚀 Starting Gunicorn..."
            exec gunicorn \
                --bind 0.0.0.0:8000 \
                --workers 3 \
                --worker-class gthread \
                --threads 2 \
                --timeout 120 \
                --keep-alive 5 \
                --max-requests 1000 \
                --max-requests-jitter 100 \
                --preload \
                --access-logfile - \
                --error-logfile - \
                --log-level info \
                sistema_produtos.wsgi:application
            ;;
        "migrate")
            echo "🗄️ Running migrations only..."
            wait_for_db
            run_migrations
            ;;
        "collectstatic")
            echo "📦 Collecting static files only..."
            collect_static
            ;;
        "setup")
            echo "⚙️ Running full setup..."
            wait_for_db
            wait_for_redis
            run_migrations
            collect_static
            create_cache_table
            validate_django
            echo "✅ Setup completed!"
            ;;
        "shell")
            echo "🐚 Starting Django shell..."
            wait_for_db
            exec python manage.py shell
            ;;
        "createsuperuser")
            echo "👤 Creating superuser..."
            wait_for_db
            exec python manage.py createsuperuser
            ;;
        "test")
            echo "🧪 Running tests..."
            wait_for_db
            exec python manage.py test
            ;;
        *)
            echo "🔧 Running custom command: $*"
            wait_for_db
            exec "$@"
            ;;
    esac
}

# Check if running as root and warn
if [ "$(id -u)" = "0" ]; then
    echo "⚠️ WARNING: Running as root user. This is not recommended for production."
fi

# Set default timezone if not set
export TZ=${TZ:-UTC}

# Run main function with all arguments
main "$@"
