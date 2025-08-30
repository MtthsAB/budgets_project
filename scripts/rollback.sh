#!/bin/bash

# =====================================
# ROLLBACK SCRIPT
# =====================================
# Quick rollback to previous version in case of deployment issues

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
NC='\033[0m'

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

# Get list of available versions
list_versions() {
    log "Available image versions:"
    docker images sistema_produtos --format "table {{.Tag}}\t{{.CreatedAt}}" | grep -v "latest"
}

# Get current running version
get_current_version() {
    local container_id=$(docker-compose -f "$DOCKER_COMPOSE_FILE" ps -q web | head -1)
    if [ -n "$container_id" ]; then
        docker inspect "$container_id" --format '{{index .Config.Labels "org.opencontainers.image.version"}}'
    else
        echo "unknown"
    fi
}

# Rollback to specific version
rollback() {
    local target_version="$1"
    
    if [ -z "$target_version" ]; then
        error "Target version not specified"
        list_versions
        exit 1
    fi
    
    # Check if target image exists
    if ! docker images --format "{{.Repository}}:{{.Tag}}" | grep -q "sistema_produtos:$target_version"; then
        error "Image sistema_produtos:$target_version not found"
        list_versions
        exit 1
    fi
    
    local current_version=$(get_current_version)
    log "Current version: $current_version"
    log "Rolling back to version: $target_version"
    
    # Set environment variables
    export APP_VERSION="$target_version"
    
    # Create emergency backup
    log "Creating emergency backup before rollback..."
    local backup_dir="$PROJECT_DIR/backups"
    local backup_file="rollback_backup_$(date +%Y%m%d_%H%M%S).sql"
    
    mkdir -p "$backup_dir"
    
    if [ -f "$ENV_FILE" ]; then
        set -o allexport
        source "$ENV_FILE"
        set +o allexport
    fi
    
    docker-compose -f "$DOCKER_COMPOSE_FILE" --env-file "$ENV_FILE" exec -T db \
        pg_dump -U "$DB_USER" "$DB_NAME" > "$backup_dir/$backup_file"
    gzip "$backup_dir/$backup_file"
    
    success "Emergency backup created: $backup_dir/${backup_file}.gz"
    
    # Perform rollback
    log "Performing rollback..."
    
    # Update containers with target version
    docker-compose -f "$DOCKER_COMPOSE_FILE" --env-file "$ENV_FILE" \
        up -d --no-deps web
    
    # Wait for health check
    log "Waiting for application to be healthy..."
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f -s "http://localhost/healthz/" > /dev/null; then
            success "Application is healthy after rollback"
            break
        fi
        
        log "Attempt $attempt/$max_attempts: Waiting for health check..."
        sleep 10
        ((attempt++))
    done
    
    if [ $attempt -gt $max_attempts ]; then
        error "Application failed to become healthy after rollback"
        exit 1
    fi
    
    success "🔄 Rollback to version $target_version completed successfully!"
    log "Previous version $current_version -> Current version $target_version"
}

# Print usage
usage() {
    cat << EOF
Usage: $0 [OPTIONS] [VERSION]

Rollback script for Sistema Produtos

ARGUMENTS:
    VERSION                    Target version to rollback to

OPTIONS:
    -l, --list                 List available versions
    -c, --current              Show current version
    -h, --help                 Show this help message

EXAMPLES:
    $0 -l                      # List available versions
    $0 -c                      # Show current version
    $0 v1.2.3                  # Rollback to specific version
    $0 20250830-140000         # Rollback to timestamp version

EOF
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -l|--list)
            list_versions
            exit 0
            ;;
        -c|--current)
            current_version=$(get_current_version)
            echo "Current version: $current_version"
            exit 0
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        -*)
            error "Unknown option: $1"
            usage
            exit 1
            ;;
        *)
            TARGET_VERSION="$1"
            shift
            ;;
    esac
done

# Main execution
if [ -n "$TARGET_VERSION" ]; then
    rollback "$TARGET_VERSION"
else
    warning "No target version specified"
    usage
    exit 1
fi
