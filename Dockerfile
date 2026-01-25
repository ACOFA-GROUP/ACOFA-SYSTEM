FROM python:3.11-slim

WORKDIR /code

# Installation des dépendances système pour PostgreSQL
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# On copie tout le code dans /code
COPY . .

# IMPORTANT : On force le chemin de recherche Python sur le dossier courant
ENV PYTHONPATH=/code

# On utilise la forme "module" de python pour lancer uvicorn
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
