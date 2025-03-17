import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import time

# URL de l'API FastAPI
API_URL = "http://localhost:8000"

# Charger les données du fichier CSV
df = pd.read_csv("KDDCup99.csv")

# Définir les connexions anormales et normales
df['anomaly'] = df['label'].apply(lambda x: 1 if x == 'neptune' else 0)

# Titre de l'application
st.title("📡 Simulation des Connexions Réseau - Temps Réel & Playback")

# Choix du mode
mode = st.radio("Mode de simulation", ["Playback", "Flux en temps réel"], index=0)

# Filtres interactifs
st.sidebar.header("Filtres")
protocol_list = df['protocol_type'].unique()
service_list = df['service'].unique()
selected_protocol = st.sidebar.selectbox("Protocole", ["Tous"] + list(protocol_list))
selected_service = st.sidebar.selectbox("Service", ["Tous"] + list(service_list))

# Application des filtres
filtered_df = df.copy()
if selected_protocol != "Tous":
    filtered_df = filtered_df[filtered_df['protocol_type'] == selected_protocol]
if selected_service != "Tous":
    filtered_df = filtered_df[filtered_df['service'] == selected_service]

# Affichage des données
st.write("### Connexions Réseau")
st.dataframe(filtered_df.head(1000))

# Visualisation des connexions réseau
st.write("### Visualisation des Flux Réseau")
fig = px.scatter(filtered_df, x="src_bytes", y="dst_bytes", color=filtered_df["anomaly"].astype(str),
                 hover_data=["protocol_type", "service", "label"],
                 title="Distribution des Anomalies")
st.plotly_chart(fig)

# Mode Playback - Simulation des connexions réseau
if mode == "Playback":
    st.write("### Mode Playback - Relecture des Données")
    playback_speed = st.slider("Vitesse de lecture (secondes par événement)", 0.1, 5.0, 1.0)
    start_playback = st.button("Lancer le Playback")

    if start_playback:
        for index, row in filtered_df.iterrows():
            st.write(f"📡 Connexion : Protocol {row['protocol_type']} | Service {row['service']} | Label {row['label']}")
            time.sleep(playback_speed)

# Mode Flux en Temps Réel
def send_to_api(row):
    data = row.to_dict()
    response = requests.post(f"{API_URL}/predict/", json=data)
    return response.json() if response.status_code == 200 else None

if mode == "Flux en temps réel":
    st.write("### Test en Temps Réel des Connexions")
    start_real_test = st.button("Démarrer le Test en Temps Réel")
    if start_real_test:
        for index, row in filtered_df.iterrows():
            result = send_to_api(row)
            if result:
                st.write(f"🔍 Connexion analysée : {row['label']} | Anomalie détectée : {result['anomaly']}")
            time.sleep(1)
