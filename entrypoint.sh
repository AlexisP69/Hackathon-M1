#!/bin/bash
 
# Lancer FastAPI via Gunicorn sur le port 8000
gunicorn -w 4 -k uvicorn.workers.UvicornWorker api:app --bind 0.0.0.0:8000 &
 
# Attendre un peu pour éviter les conflits
sleep 5
 
# Lancer Streamlit sur le port 8501
streamlit run dashboard.py --server.port 8501 --server.address 0.0.0.0 --server.enableCORS false --server.enableXsrfProtection false &

# Lancer Nginx en mode foreground
nginx -g "daemon off;"