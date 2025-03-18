from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler

# Charger les modèles préalablement enregistrés
iso_forest = joblib.load('isolation_forest.pkl')
oc_svm = joblib.load('one_class_svm.pkl')
autoencoder = load_model('autoencoder_model.h5', compile=False)  # Ne pas recompiler le modèle
scaler = joblib.load('scaler.pkl')

# Créer une instance de l'API FastAPI
app = FastAPI()

# Définir les données de prédiction attendues
class NetworkFlow(BaseModel):
    duration: float
    protocol_type: int
    service: int
    flag: int
    src_bytes: int
    dst_bytes: int
    # Ajouter les autres champs ici...

@app.post("/predict/")
def predict(flow: NetworkFlow):
    # Convertir les données en un tableau numpy
    data = np.array([[flow.duration, flow.protocol_type, flow.service, flow.flag, flow.src_bytes, flow.dst_bytes]])
    
    # Appliquer la mise à l'échelle
    data_scaled = scaler.transform(data)

    # Prédiction avec Isolation Forest
    iso_pred = iso_forest.predict(data_scaled)
    iso_anomaly = 1 if iso_pred == -1 else 0

    # Prédiction avec One-Class SVM
    svm_pred = oc_svm.predict(data_scaled)
    svm_anomaly = 1 if svm_pred == -1 else 0

    # Prédiction avec Autoencoder (MSE)
    reconstructions = autoencoder.predict(data_scaled)
    mse = np.mean(np.power(data_scaled - reconstructions, 2))
    ae_anomaly = 1 if mse > 0.01 else 0

    # Définir l'anomalie en fonction des résultats des modèles
    anomaly = max(iso_anomaly, svm_anomaly, ae_anomaly)

    return {"anomaly": anomaly}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
