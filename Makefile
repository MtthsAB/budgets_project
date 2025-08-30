# =====================================
# MAKEFILE FOR SISTEMA PRODUTOS
# =====================================
# Quick commands for development and deployment

.PHONY: help build deploy rollback logs clean test setup

# Default target
.DEFAULT_GOAL := help

# Configuration
DOCKER_COMPOSE_PROD = docker-compose -f docker-compose.prod.yml --env-file .env.prod
DOCKER_COMPOSE_DEV = docker-compose -f docker-compose.yml --env-file .env

# Get current timestamp for versioning
TIMESTAMP := $(shell date +%Y%m%d-%H%M%S)
GIT_HASH := $(shell git rev-parse --short HEAD 2>/dev/null || echo 'unknown')
APP_VERSION ?= $(TIMESTAMP)-$(GIT_HASH)

help: ## Show this help message
	@echo "Sistema Produtos - Available Commands"
	@echo "====================================="
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Development Commands
setup: ## Setup development environment
	@echo "Setting up development environment..."
	cp .env.example .env
	$(DOCKER_COMPOSE_DEV) build
	$(DOCKER_COMPOSE_DEV) up -d
	$(DOCKER_COMPOSE_DEV) exec app python manage.py migrate
	$(DOCKER_COMPOSE_DEV) exec app python manage.py collectstatic --noinput
	@echo "✅ Development environment ready!"

dev-up: ## Start development environment
	$(DOCKER_COMPOSE_DEV) up -d

dev-down: ## Stop development environment
	$(DOCKER_COMPOSE_DEV) down

dev-logs: ## Show development logs
	$(DOCKER_COMPOSE_DEV) logs -f

dev-shell: ## Access Django shell in development
	$(DOCKER_COMPOSE_DEV) exec app python manage.py shell

dev-test: ## Run tests in development environment
	$(DOCKER_COMPOSE_DEV) exec app python manage.py test

# Production Commands
build: ## Build production Docker image
	@echo "Building production image with version: $(APP_VERSION)"
	@export APP_VERSION=$(APP_VERSION) && \
	export BUILD_DATE=$(shell date -u +%Y-%m-%dT%H:%M:%SZ) && \
	export VCS_REF=$(GIT_HASH) && \
	docker build \
		--build-arg APP_VERSION=$$APP_VERSION \
		--build-arg BUILD_DATE=$$BUILD_DATE \
		--build-arg VCS_REF=$$VCS_REF \
		-t sistema_produtos:$$APP_VERSION \
		-t sistema_produtos:latest \
		.

deploy: ## Deploy to production with zero downtime
	@echo "Starting production deployment..."
	./scripts/deploy.sh -v $(APP_VERSION)

deploy-quick: ## Quick deploy without backup
	@echo "Starting quick deployment (no backup)..."
	./scripts/deploy.sh -v $(APP_VERSION) --skip-backup

rollback: ## Rollback to previous version (specify VERSION=xxx)
	@if [ -z "$(VERSION)" ]; then \
		echo "Please specify VERSION. Usage: make rollback VERSION=v1.2.3"; \
		./scripts/rollback.sh --list; \
	else \
		./scripts/rollback.sh $(VERSION); \
	fi

prod-up: ## Start production environment
	@export APP_VERSION=$(APP_VERSION) && $(DOCKER_COMPOSE_PROD) up -d

prod-down: ## Stop production environment
	$(DOCKER_COMPOSE_PROD) down

prod-logs: ## Show production logs
	$(DOCKER_COMPOSE_PROD) logs -f

prod-status: ## Show production container status
	$(DOCKER_COMPOSE_PROD) ps

# Database Commands
backup: ## Create database backup
	@echo "Creating database backup..."
	mkdir -p backups
	$(DOCKER_COMPOSE_PROD) exec -T db pg_dump -U $$DB_USER $$DB_NAME > backups/backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "✅ Backup created in backups/ directory"

restore: ## Restore database backup (specify BACKUP=filename)
	@if [ -z "$(BACKUP)" ]; then \
		echo "Please specify BACKUP file. Usage: make restore BACKUP=backup_20250830_140000.sql"; \
		echo "Available backups:"; \
		ls -la backups/; \
	else \
		echo "Restoring backup: $(BACKUP)"; \
		$(DOCKER_COMPOSE_PROD) exec -T db psql -U $$DB_USER $$DB_NAME < backups/$(BACKUP); \
	fi

migrate: ## Run database migrations
	$(DOCKER_COMPOSE_PROD) exec app python manage.py migrate

# Maintenance Commands
clean: ## Clean Docker system
	@echo "Cleaning Docker system..."
	docker system prune -f
	docker image prune -f
	docker volume prune -f

clean-all: ## Clean Docker system including volumes (DANGEROUS)
	@echo "⚠️  WARNING: This will remove all Docker data including volumes!"
	@read -p "Are you sure? (y/N): " confirm && [ "$$confirm" = "y" ] || exit 1
	docker system prune -a -f --volumes

logs: ## Show application logs
	$(DOCKER_COMPOSE_PROD) logs -f web

health: ## Check application health
	@echo "Checking application health..."
	@curl -f http://localhost/healthz/ && echo "✅ Application is healthy" || echo "❌ Application is unhealthy"

# Security Commands
security-scan: ## Run security scan on Docker image
	@echo "Running security scan..."
	docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
		aquasec/trivy image sistema_produtos:latest

update-deps: ## Update Python dependencies
	@echo "Checking for dependency updates..."
	docker run --rm -v $(PWD):/app -w /app python:3.10-slim \
		bash -c "pip install pip-tools && pip-compile --upgrade requirements.in"

# Monitoring Commands
stats: ## Show container resource usage
	docker stats $(shell $(DOCKER_COMPOSE_PROD) ps -q)

top: ## Show top processes in containers
	@echo "Web container processes:"
	$(DOCKER_COMPOSE_PROD) exec web ps aux
	@echo "\nDatabase container processes:"
	$(DOCKER_COMPOSE_PROD) exec db ps aux

# Development Helpers
shell: ## Access application shell
	$(DOCKER_COMPOSE_PROD) exec app bash

db-shell: ## Access database shell
	$(DOCKER_COMPOSE_PROD) exec db psql -U $$DB_USER $$DB_NAME

create-superuser: ## Create Django superuser
	$(DOCKER_COMPOSE_PROD) exec app python manage.py createsuperuser

collectstatic: ## Collect static files
	$(DOCKER_COMPOSE_PROD) exec app python manage.py collectstatic --noinput

# Release Commands
release: ## Create a new release (specify VERSION=vX.Y.Z)
	@if [ -z "$(VERSION)" ]; then \
		echo "Please specify VERSION. Usage: make release VERSION=v1.2.3"; \
		exit 1; \
	fi
	@echo "Creating release $(VERSION)..."
	git tag -a $(VERSION) -m "Release $(VERSION)"
	git push origin $(VERSION)
	@echo "✅ Release $(VERSION) created and pushed"

list-versions: ## List available image versions
	@echo "Available image versions:"
	docker images sistema_produtos --format "table {{.Tag}}\t{{.CreatedAt}}\t{{.Size}}"

# Quick status check
status: ## Show overall system status
	@echo "=== Sistema Produtos Status ==="
	@echo "Current time: $(shell date)"
	@echo "Git branch: $(shell git branch --show-current 2>/dev/null || echo 'unknown')"
	@echo "Git hash: $(GIT_HASH)"
	@echo "App version: $(APP_VERSION)"
	@echo ""
	@echo "=== Container Status ==="
	@$(DOCKER_COMPOSE_PROD) ps
	@echo ""
	@echo "=== Health Check ==="
	@curl -s http://localhost/healthz/ | python -m json.tool 2>/dev/null || echo "Health check failed"
