#!/bin/bash

# =====================================
# ZERO DOWNTIME DEPLOYMENT SCRIPT
# =====================================
# This script implements a zero-downtime deployment strategy
# for the Sistema Produtos Django application

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
DOCKER_COMPOSE_FILE="$PROJECT_DIR/docker-compose.prod.yml"
ENV_FILE="$PROJECT_DIR/.env.prod"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
APP_VERSION="${APP_VERSION:-$(date +%Y%m%d-%H%M%S)}"
BUILD_DATE="${BUILD_DATE:-$(date -u +%Y-%m-%dT%H:%M:%SZ)}"
VCS_REF="${VCS_REF:-$(git rev-parse --short HEAD 2>/dev/null || echo 'unknown')}"
SKIP_BACKUP="${SKIP_BACKUP:-false}"
SKIP_TESTS="${SKIP_TESTS:-false}"
REGISTRY="${REGISTRY:-ghcr.io/z-matas}"
IMAGE_NAME="${IMAGE_NAME:-sistema-produtos}"

# Functions
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Check if required files exist
check_prerequisites() {
    log "Checking prerequisites..."
    
    if [ ! -f "$DOCKER_COMPOSE_FILE" ]; then
        error "Docker Compose file not found: $DOCKER_COMPOSE_FILE"
        exit 1
    fi
    
    if [ ! -f "$ENV_FILE" ]; then
        error "Environment file not found: $ENV_FILE"
        exit 1
    fi
    
    if ! command -v docker &> /dev/null; then
        error "Docker is not installed or not in PATH"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose is not installed or not in PATH"
        exit 1
    fi
    
    success "Prerequisites check passed"
}

# Create backup of database
create_backup() {
    if [ "$SKIP_BACKUP" = "true" ]; then
        warning "Skipping database backup"
        return 0
    fi
    
    log "Creating database backup..."
    
    local backup_dir="$PROJECT_DIR/backups"
    local backup_file="backup_$(date +%Y%m%d_%H%M%S).sql"
    
    mkdir -p "$backup_dir"
    
    # Create backup using existing database container
    docker-compose -f "$DOCKER_COMPOSE_FILE" --env-file "$ENV_FILE" exec -T db \
        pg_dump -U "$DB_USER" "$DB_NAME" > "$backup_dir/$backup_file"
    
    # Compress backup
    gzip "$backup_dir/$backup_file"
    
    success "Database backup created: $backup_dir/${backup_file}.gz"
    
    # Keep only last 7 backups
    find "$backup_dir" -name "backup_*.sql.gz" -mtime +7 -delete
    log "Old backups cleaned up (keeping last 7 days)"
}

# Build and tag Docker image
build_image() {
    log "Building Docker image with version: $APP_VERSION"
    
    cd "$PROJECT_DIR"
    
    # Build image with version tags
    docker build \
        --build-arg APP_VERSION="$APP_VERSION" \
        --build-arg BUILD_DATE="$BUILD_DATE" \
        --build-arg VCS_REF="$VCS_REF" \
        -t "$IMAGE_NAME:$APP_VERSION" \
        -t "$IMAGE_NAME:latest" \
        .
    
    success "Docker image built successfully"
}

# Push image to registry
push_image() {
    if [ -n "$REGISTRY" ]; then
        log "Pushing image to registry: $REGISTRY"
        
        # Tag for registry
        docker tag "$IMAGE_NAME:$APP_VERSION" "$REGISTRY/$IMAGE_NAME:$APP_VERSION"
        docker tag "$IMAGE_NAME:latest" "$REGISTRY/$IMAGE_NAME:latest"
        
        # Push to registry
        docker push "$REGISTRY/$IMAGE_NAME:$APP_VERSION"
        docker push "$REGISTRY/$IMAGE_NAME:latest"
        
        success "Image pushed to registry"
    else
        log "No registry configured, skipping push"
    fi
}

# Run pre-deployment setup (migrations, collectstatic)
run_setup() {
    log "Running pre-deployment setup..."
    
    # Set environment variables for this operation
    export APP_VERSION
    export BUILD_DATE
    export VCS_REF
    
    # Run setup job (migrations and collectstatic)
    docker-compose -f "$DOCKER_COMPOSE_FILE" --env-file "$ENV_FILE" \
        run --rm --no-deps app-setup
    
    success "Pre-deployment setup completed"
}

# Deploy new version with zero downtime
deploy() {
    log "Starting zero-downtime deployment..."
    
    # Set environment variables
    export APP_VERSION
    export BUILD_DATE
    export VCS_REF
    
    # Scale up new web container(s) alongside existing ones
    log "Scaling up new web containers..."
    docker-compose -f "$DOCKER_COMPOSE_FILE" --env-file "$ENV_FILE" \
        up -d --no-deps --scale web=2 web
    
    # Wait for new containers to be healthy
    log "Waiting for new containers to be healthy..."
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if docker-compose -f "$DOCKER_COMPOSE_FILE" --env-file "$ENV_FILE" \
           exec -T web curl -f http://localhost:8000/healthz/ > /dev/null 2>&1; then
            success "New containers are healthy"
            break
        fi
        
        log "Attempt $attempt/$max_attempts: Waiting for containers to be healthy..."
        sleep 10
        ((attempt++))
    done
    
    if [ $attempt -gt $max_attempts ]; then
        error "New containers failed to become healthy"
        log "Rolling back..."
        docker-compose -f "$DOCKER_COMPOSE_FILE" --env-file "$ENV_FILE" \
            down --remove-orphans
        exit 1
    fi
    
    # Reload Nginx to pick up new backend servers
    log "Reloading Nginx configuration..."
    docker-compose -f "$DOCKER_COMPOSE_FILE" --env-file "$ENV_FILE" \
        exec nginx nginx -s reload || warning "Nginx reload failed"
    
    # Stop old containers
    log "Stopping old containers..."
    # This would require a more sophisticated approach in a real blue-green setup
    # For now, we'll restart the service
    docker-compose -f "$DOCKER_COMPOSE_FILE" --env-file "$ENV_FILE" \
        up -d --no-deps web
    
    success "Deployment completed successfully"
}

# Run smoke tests
run_tests() {
    if [ "$SKIP_TESTS" = "true" ]; then
        warning "Skipping smoke tests"
        return 0
    fi
    
    log "Running smoke tests..."
    
    # Test health endpoint
    if curl -f -s "http://localhost/healthz/" > /dev/null; then
        success "Health endpoint test passed"
    else
        error "Health endpoint test failed"
        return 1
    fi
    
    # Test main page
    if curl -f -s "http://localhost/" > /dev/null; then
        success "Main page test passed"
    else
        error "Main page test failed"
        return 1
    fi
    
    # Test admin page
    if curl -f -s "http://localhost/admin/" > /dev/null; then
        success "Admin page test passed"
    else
        warning "Admin page test failed (might require authentication)"
    fi
    
    success "Smoke tests completed"
}

# Cleanup old images
cleanup() {
    log "Cleaning up old Docker images..."
    
    # Remove old images (keep last 5 versions)
    docker images "$IMAGE_NAME" --format "table {{.Tag}}\t{{.ID}}" | \
        grep -v "latest" | tail -n +6 | awk '{print $2}' | xargs -r docker rmi || true
    
    # Remove dangling images
    docker image prune -f
    
    success "Cleanup completed"
}

# Print usage
usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Zero-downtime deployment script for Sistema Produtos

OPTIONS:
    -v, --version VERSION       Set application version (default: timestamp)
    -r, --registry REGISTRY     Docker registry URL
    -s, --skip-backup          Skip database backup
    -t, --skip-tests           Skip smoke tests
    -b, --build-only           Only build image, don't deploy
    -d, --deploy-only          Only deploy, don't build
    -h, --help                 Show this help message

EXAMPLES:
    $0                         # Full deployment with auto-generated version
    $0 -v v1.2.3              # Deploy specific version
    $0 --skip-backup           # Deploy without backup
    $0 --build-only -v v1.2.3  # Only build image
    $0 --deploy-only           # Only deploy existing image

ENVIRONMENT VARIABLES:
    APP_VERSION               Application version
    BUILD_DATE               Build timestamp
    VCS_REF                  Git commit hash
    REGISTRY                 Docker registry URL
    DB_USER                  Database user
    DB_NAME                  Database name
    SKIP_BACKUP             Skip backup (true/false)
    SKIP_TESTS              Skip tests (true/false)

EOF
}

# Parse command line arguments
BUILD_ONLY=false
DEPLOY_ONLY=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -v|--version)
            APP_VERSION="$2"
            shift 2
            ;;
        -r|--registry)
            REGISTRY="$2"
            shift 2
            ;;
        -s|--skip-backup)
            SKIP_BACKUP=true
            shift
            ;;
        -t|--skip-tests)
            SKIP_TESTS=true
            shift
            ;;
        -b|--build-only)
            BUILD_ONLY=true
            shift
            ;;
        -d|--deploy-only)
            DEPLOY_ONLY=true
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            error "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

# Main execution
main() {
    log "Starting deployment process..."
    log "Version: $APP_VERSION"
    log "Build Date: $BUILD_DATE"
    log "VCS Ref: $VCS_REF"
    
    # Load environment variables
    if [ -f "$ENV_FILE" ]; then
        set -o allexport
        source "$ENV_FILE"
        set +o allexport
    fi
    
    check_prerequisites
    
    if [ "$DEPLOY_ONLY" = "false" ]; then
        build_image
        push_image
    fi
    
    if [ "$BUILD_ONLY" = "false" ]; then
        create_backup
        run_setup
        deploy
        run_tests
        cleanup
        
        success "🚀 Deployment completed successfully!"
        log "Application version $APP_VERSION is now live"
        log "Health check: http://localhost/healthz/"
    else
        success "🏗️ Build completed successfully!"
        log "Image built: $IMAGE_NAME:$APP_VERSION"
    fi
}

# Execute main function
main "$@"
