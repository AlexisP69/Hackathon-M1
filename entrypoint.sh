#!/bin/bash

# Lancer FastAPI via Gunicorn sur le port 80
gunicorn -w 4 -k uvicorn.workers.UvicornWorker api:app --bind 0.0.0.0:80 &

# Lancer Streamlit sur le même port avec un subpath
streamlit run dashboard.py --server.port 80 --server.address 0.0.0.0 --server.baseUrlPath /streamlit
