# Run the project
dev:
	docker compose up

dev-build:
	docker compose up --build

# Stop the project
down:
	docker compose down

# Purge containers and database volume
clean:
	docker compose down -v

# Sync uv.lock
lock:
	docker compose exec web uv lock

# Django database operations
migrations:
	docker compose exec web uv run manage.py makemigrations

migrate:
	docker compose exec web uv run manage.py migrate

# Create Django admin user
superuser:
	docker compose exec web uv run manage.py createsuperuser

# Reset database from scratch
reset-db:
	docker compose down -v
	docker compose up -d
	docker compose exec web uv run manage.py migrate