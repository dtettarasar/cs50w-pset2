# Démarrage
dev:
	docker compose up

dev-build:
	docker compose up --build

# Arret
down:
	docker compose down

# Purge complète (supprime les conteneurs ET les volumes de données)
clean:
	docker compose down -v

# Mettre à jour / synchroniser le uv.lock
lock:
	docker compose exec web uv lock

# Migrations Django
migrations:
	docker compose exec web uv run manage.py makemigrations

migrate:
	docker compose exec web uv run manage.py migrate

# Commande pratique pour tout réinitialiser proprement à neuf
reset-db:
	docker compose down -v
	docker compose up -d
	docker compose exec web uv run manage.py migrate