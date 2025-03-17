from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
import numpy as np
import joblib
import tensorflow as tf

# Charger les modèles
oc_svm = joblib.load("one_class_svm.pkl")

autoencoder = tf.keras.models.load_model("autoencoder_model.h5", compile=False)

scaler = joblib.load("scaler.pkl")

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["network_security"]
collection = db["logs"]

# Création de l'API FastAPI
app = FastAPI()

# Modèle de requête
class NetworkFlow(BaseModel):
    duration: float
    protocol_type: int
    service: int
    flag: int
    src_bytes: int
    dst_bytes: int
    land: int
    wrong_fragment: int
    urgent: int
    hot: int
    num_failed_logins: int
    logged_in: int
    num_compromised: int
    root_shell: int
    su_attempted: int
    num_root: int
    num_file_creations: int
    num_shells: int
    num_access_files: int
    num_outbound_cmds: int
    is_host_login: int
    is_guest_login: int
    count: int
    srv_count: int
    serror_rate: float
    srv_serror_rate: float
    rerror_rate: float
    srv_rerror_rate: float
    same_srv_rate: float
    diff_srv_rate: float
    srv_diff_host_rate: float
    dst_host_count: int
    dst_host_srv_count: int
    dst_host_same_srv_rate: float
    dst_host_diff_srv_rate: float
    dst_host_same_src_port_rate: float
    dst_host_srv_diff_host_rate: float
    dst_host_serror_rate: float
    dst_host_srv_serror_rate: float
    dst_host_rerror_rate: float
    dst_host_srv_rerror_rate: float

@app.post("/predict/")
def detect_anomaly(flow: NetworkFlow):
    data = np.array([list(flow.dict().values())]).astype(float)
    data = scaler.transform(data)

    # Prédiction One-Class SVM
    pred_svm = oc_svm.predict(data)
    anomaly_svm = 1 if pred_svm[0] == -1 else 0

    # Prédiction Autoencoder
    reconstructions = autoencoder.predict(data)
    mse = np.mean(np.power(data - reconstructions, 2))
    anomaly_ae = 1 if mse > 0.01 else 0  # Seuil ajustable

    # Détection finale
    anomaly = max(anomaly_svm, anomaly_ae)
    result = {"anomaly": anomaly, "flow": flow.dict()}
    collection.insert_one(result)
    return result

@app.get("/anomalies/")
def get_anomalies():
    anomalies = list(collection.find({"anomaly": 1}, {"_id": 0}))
    return {"anomalies": anomalies}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
