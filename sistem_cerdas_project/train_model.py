import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression

# 1. Baca dataset smartphone
df = pd.read_csv("Smartphone.csv")

# 2. Tentukan fitur (X) dan target (y)
X = df[["ram_gb", "storage_gb", "baterai_mah", "kamera_mp"]]
y = df["harga_juta"]

# 3. Latih model regresi linear
model = LinearRegression().fit(X, y)

# 4. Simpan model ke file .joblib
joblib.dump(model, "model_smartphone.joblib")
print("Model berhasil dilatih dan disimpan ke model_smartphone.joblib!")