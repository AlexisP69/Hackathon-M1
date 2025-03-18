import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import time
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# URL de l'API FastAPI
API_URL = "http://localhost:8000"

# Charger les données du fichier CSV
df = pd.read_csv("KDDCup99.csv")

# Définir les connexions anormales et normales
df['anomaly'] = df['label'].apply(lambda x: 0 if x == 'normal' else 1)
df.drop(columns=['label'], inplace=True)

# Pipeline pour la normalisation
scaler = StandardScaler()
pipeline = Pipeline([('scaler', scaler)])

# Titre de l'application
st.title("📡 Analyse des Connexions Réseau - Anomalies & Comparaisons")

# Filtres interactifs
st.sidebar.header("Filtres")

# Filtres principaux : protocole, service, IP, anomalie
protocol_list = df['protocol_type'].unique()
service_list = df['service'].unique()
ip_list = df['src_bytes'].unique()

selected_protocol = st.sidebar.selectbox("Protocole", ["Tous"] + list(protocol_list))
selected_service = st.sidebar.selectbox("Service", ["Tous"] + list(service_list))
selected_ip = st.sidebar.selectbox("IP Source", ["Tous"] + list(ip_list))
selected_anomaly = st.sidebar.selectbox("Anomalie", ["Tous", "Normal", "Anomalie"])

# Appliquer les filtres
filtered_df = df.copy()
if selected_protocol != "Tous":
    filtered_df = filtered_df[filtered_df['protocol_type'] == selected_protocol]
if selected_service != "Tous":
    filtered_df = filtered_df[filtered_df['service'] == selected_service]
if selected_ip != "Tous":
    filtered_df = filtered_df[filtered_df['src_bytes'] == selected_ip]
if selected_anomaly != "Tous":
    anomaly_filter = 0 if selected_anomaly == "Normal" else 1
    filtered_df = filtered_df[filtered_df['anomaly'] == anomaly_filter]

# Affichage des données filtrées
st.write("### Connexions Réseau Filtrées")
st.dataframe(filtered_df.head(1000))

# --- Graphiques analytiques de base ---

# 1. Histogramme des anomalies par protocole
st.write("### Histogramme des Anomalies par Protocole")
if filtered_df['protocol_type'].notnull().sum() > 0:
    fig_hist_protocol = px.histogram(filtered_df, x='protocol_type', color='anomaly', barmode='group',
                                      title="Comparaison des Anomalies par Protocole")
    st.plotly_chart(fig_hist_protocol)
else:
    st.write("Pas de données pour afficher l'histogramme des anomalies par protocole.")

# 2. Histogramme des anomalies par service
st.write("### Histogramme des Anomalies par Service")
if filtered_df['service'].notnull().sum() > 0:
    fig_service = px.histogram(filtered_df, x='service', color='anomaly', barmode='group',
                                title="Comparaison des Anomalies par Service")
    st.plotly_chart(fig_service)
else:
    st.write("Pas de données pour afficher l'histogramme des anomalies par service.")

# 3. Histogramme des anomalies par source de bytes
st.write("### Histogramme des Anomalies par Source de Bytes")
if filtered_df['src_bytes'].sum() > 0:
    fig_bytes = px.histogram(filtered_df, x='src_bytes', color='anomaly', barmode='group',
                              title="Comparaison des Anomalies par Nombre de Bytes Source")
    st.plotly_chart(fig_bytes)
else:
    st.write("Pas de données pour afficher l'histogramme des anomalies par source de bytes.")

# 4. Répartition des anomalies vs connexions normales
st.write("### Répartition des Anomalies vs Connexions Normales")
if filtered_df['anomaly'].value_counts().sum() > 0:
    anomaly_counts = filtered_df['anomaly'].value_counts()
    fig_pie = px.pie(names=['Normal', 'Anomalie'], values=anomaly_counts, title="Proportion des Anomalies dans le Dataset")
    st.plotly_chart(fig_pie)
else:
    st.write("Pas de données pour afficher la répartition des anomalies.")

# 5. Boxplot des anomalies par nombre de connexions
st.write("### Boxplot des Anomalies par Nombre de Connexions")
if filtered_df['count'].sum() > 0:
    fig_box = px.box(filtered_df, x="anomaly", y="count", title="Boxplot des Anomalies par Nombre de Connexions")
    st.plotly_chart(fig_box)
else:
    st.write("Pas de données pour afficher le boxplot des anomalies.")

# 6. Heatmap des anomalies par protocole et service
st.write("### Heatmap des Anomalies par Protocole et Service")
if filtered_df[['protocol_type', 'service']].notnull().all(axis=1).sum() > 0:
    fig_heatmap = px.density_heatmap(filtered_df, x="protocol_type", y="service", z="anomaly",
                                     title="Heatmap des Anomalies par Protocole et Service")
    st.plotly_chart(fig_heatmap)
else:
    st.write("Pas de données pour afficher la heatmap des anomalies par protocole et service.")

# 7. Distribution des anomalies par erreur rate
st.write("### Distribution des Anomalies par Erreur Rate")
if filtered_df['serror_rate'].sum() > 0:
    fig_error_rate = px.histogram(filtered_df, x="serror_rate", color="anomaly", title="Erreur Rate des Anomalies")
    st.plotly_chart(fig_error_rate)
else:
    st.write("Pas de données pour afficher la distribution des anomalies par erreur rate.")

# 8. Répartition des anomalies par nombre de tentatives de login
st.write("### Anomalies par Nombre de Tentatives de Connexion")
if filtered_df['num_failed_logins'].sum() > 0:
    fig_attempts = px.histogram(filtered_df, x="num_failed_logins", color="anomaly", barmode='group',
                                 title="Comparaison des Anomalies par Nombre de Tentatives de Connexion")
    st.plotly_chart(fig_attempts)
else:
    st.write("Pas de données pour afficher les anomalies par nombre de tentatives de connexion.")

# 9. Graphique des anomalies par nombre de fichiers créés
st.write("### Anomalies par Nombre de Fichiers Créés")
if filtered_df['lnum_file_creations'].sum() > 0:
    fig_file_creations = px.histogram(filtered_df, x="lnum_file_creations", color="anomaly", barmode='group',
                                      title="Comparaison des Anomalies par Nombre de Fichiers Créés")
    st.plotly_chart(fig_file_creations)
else:
    st.write("Pas de données pour afficher les anomalies par nombre de fichiers créés.")

# 10. Graphique des anomalies par nombre de connexions sortantes
st.write("### Anomalies par Nombre de Connexions Sortantes")
if filtered_df['lnum_outbound_cmds'].sum() > 0:
    fig_outbound = px.histogram(filtered_df, x="lnum_outbound_cmds", color="anomaly", barmode='group',
                                 title="Comparaison des Anomalies par Nombre de Connexions Sortantes")
    st.plotly_chart(fig_outbound)
else:
    st.write("Pas de données pour afficher les anomalies par connexions sortantes.")
