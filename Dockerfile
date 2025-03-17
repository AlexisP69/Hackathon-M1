# Utilisation de Python 3.12 comme base
FROM python:3.12

# Définition du répertoire de travail
WORKDIR /app

# Copier les fichiers du projet
COPY . /app

# Mise à jour de pip et installation des dépendances
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir tensorflow pandas numpy scikit-learn fastapi uvicorn streamlit requests joblib plotly pymongo

# Exposition du port 80 (pas 443)
EXPOSE 80

# Lancer les services avec un script
CMD ["bash", "entrypoint.sh"]
