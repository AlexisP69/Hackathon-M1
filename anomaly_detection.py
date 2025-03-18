import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.neighbors import LocalOutlierFactor
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
import joblib

# Charger le dataset KDD Cup 99
df = pd.read_csv("KDDCup99.csv")

# Encoder les variables catégoriques
for col in ["protocol_type", "service", "flag"]:
    df[col] = LabelEncoder().fit_transform(df[col])

# Correction des labels (0 = normal, 1 = anomalie)
df['anomaly'] = df['label'].apply(lambda x: 0 if x == 'normal' else 1)
df.drop(columns=['label'], inplace=True)

# Normalisation des données
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df.drop(columns=['anomaly']))  # Exclure la colonne d'anomalie

# Séparation des données en train et test
X_train, X_test, y_train, y_test = train_test_split(df_scaled, df['anomaly'], test_size=0.2, random_state=42, stratify=df['anomaly'])

# Entraînement Isolation Forest
iso_forest = IsolationForest(n_estimators=200, contamination=0.05, random_state=42)
iso_forest.fit(X_train)
joblib.dump(iso_forest, "isolation_forest.pkl")

# Entraînement One-Class SVM
oc_svm = OneClassSVM(nu=0.03, kernel="rbf", gamma="scale")  # Réduction du nu pour moins de faux positifs
oc_svm.fit(X_train)
joblib.dump(oc_svm, "one_class_svm.pkl")

# Entraînement Local Outlier Factor (LOF)
lof = LocalOutlierFactor(n_neighbors=20, contamination=0.05)
lof.fit(X_train)
joblib.dump(lof, "lof.pkl")

# Entraînement Autoencoder amélioré
input_dim = X_train.shape[1]

autoencoder = Sequential([
    Dense(128, activation='relu', input_shape=(input_dim,)),
    BatchNormalization(),
    Dropout(0.3),
    Dense(64, activation='relu'),
    BatchNormalization(),
    Dense(32, activation='relu'),
    Dense(64, activation='relu'),
    BatchNormalization(),
    Dropout(0.3),
    Dense(128, activation='relu'),
    Dense(input_dim, activation='tanh')
])

autoencoder.compile(optimizer=Adam(learning_rate=0.0001), loss='mse')
autoencoder.fit(X_train, X_train, epochs=50, batch_size=64, validation_data=(X_test, X_test), verbose=1)

# Sauvegarde du modèle Autoencoder
autoencoder.save("autoencoder_model.h5")

# Sauvegarde du scaler
joblib.dump(scaler, "scaler.pkl")

print("✅ Modèles améliorés et sauvegardés !")