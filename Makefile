# ----- DEVELOPMENT -----

dev:
	docker compose up

dev-detach:
	docker compose up -d

dev-build:
	docker compose up --build

down:
	docker compose down

# Stop containers and delete local DB volume
down-v:
	docker compose down -v

# ----- DJANGO MANAGEMENT -----

migrations:
	docker compose exec web uv run manage.py makemigrations

migrate:
	docker compose exec web uv run manage.py migrate

superuser:
	docker compose exec web uv run manage.py createsuperuser

# Reset DB volume and re-apply migrations from scratch
reset-db:
	docker compose down -v
	docker compose up -d
	docker compose exec web uv run manage.py migrate

lock:
	docker compose exec web uv lock

# ----- MONITORING & LOGS -----

# List running containers
ps:
	docker compose ps

# Follow application logs in real-time
logs:
	docker compose logs -f

# ----- MAINTENANCE & CLEANUP -----

# Show Docker disk usage
df:
	docker system df

# Remove stopped containers and dangling images
clean:
	docker system prune -f

# Deep cleanup: remove unused images, volumes, and build cache
clean-all:
	docker system prune -a --volumes -f
	docker builder prune -a -f

# Clean build cache only
clean-cache:
	docker builder prune -a -f