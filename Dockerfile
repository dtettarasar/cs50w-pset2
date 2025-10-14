# Utilise une image Python officielle
FROM python:3.12-slim

# Configure l'environnement
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Crée le répertoire de travail dans le conteneur
WORKDIR /app

# Copie les fichiers du projet
COPY . .

# Installe uv
RUN pip install --no-cache-dir uv

# Installe les dépendances via uv
RUN uv sync --frozen --no-dev

# Expose le port de Django
EXPOSE 8000

# Commande de lancement du serveur Django
CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
