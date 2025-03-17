#!/bin/bash

# Lancer FastAPI en arrière-plan sur le port 80
uvicorn api:app --host 0.0.0.0 --port 80 &

# Lancer Streamlit sur le port 80
streamlit run dashboard.py --server.port 80 --server.address 0.0.0.0
