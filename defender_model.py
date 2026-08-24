import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
from xgboost import XGBClassifier

print("Loading simulation dataset...")
data_path = Path(__file__).resolve().parent / 'master_payment_simulation.csv'
df = pd.read_csv(data_path)

# Define features for our classifier
features = ['amount', 'device_trust_score', 'velocity_1h', 'biometric_variance']
X = df[features]
y = df['is_fraud']

# Split data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print("Training XGBoost Defender Model...")
model = XGBClassifier(n_estimators=100, max_depth=5, learning_rate=0.1, random_state=42)
model.fit(X_train, y_train)

# Evaluate performance
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

print("\n--- BLUE TEAM DEFENDER PERFORMANCE REPORT ---")
print(classification_report(y_test, y_pred))
print(f"ROC-AUC Score: {roc_auc_score(y_test, y_prob):.4f}")
