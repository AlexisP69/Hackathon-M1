#!/bin/bash

# Lancer FastAPI via Gunicorn sur le port 80
gunicorn -w 4 -k uvicorn.workers.UvicornWorker api:app --bind 0.0.0.0:80 &

# Attendre un peu pour éviter les conflits
sleep 5

# Lancer Streamlit sur le port 8501
streamlit run dashboard.py --server.port 8501 --server.address 0.0.0.0 --server.baseUrlPath /streamlit
