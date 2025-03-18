# Utiliser une image Python officielle
FROM python:3.12

# Installer Nginx
RUN apt-get update && apt-get install -y nginx && apt-get clean
 
# Définir le répertoire de travail
WORKDIR /app
 
# Copier les fichiers du projet
COPY . /app
 
# Copier la configuration Nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port pour nginx FastAPI (8000) et Streamlit (8501)
EXPOSE 80

# Rendre exécutable l'entrypoint
RUN chmod +x entrypoint.sh

# Lancer l'application via un script d'entrée (entrypoint.sh)
CMD ["bash", "entrypoint.sh"]
