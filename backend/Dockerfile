FROM python:3.11-slim

# Création d'un utilisateur non-root pour la sécurité
RUN useradd -m appuser
WORKDIR /app

# Installation des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code et changement de propriétaire
COPY . .
RUN chown -R appuser:appuser /app

USER appuser
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]