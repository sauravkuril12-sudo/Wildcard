import pandas as pd
from pathlib import Path
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, recall_score

DEFAULT_DATA_PATH = Path(__file__).parent / "data" / "master_payment_simulation.csv"


def train_defender_model(csv_path=DEFAULT_DATA_PATH, mutation_boost=False):
    df = pd.read_csv(csv_path)
    
    # If Gen-2 mutation is active, synthetically reinforce missed patterns
    if mutation_boost:
        # Hardening simulation: upweight complex fraud samples
        fraud_subset = df[df['is_fraud'] == 1].copy()
        df = pd.concat([df, fraud_subset, fraud_subset], ignore_index=True)

    features = ['amount', 'device_trust_score', 'velocity_1h', 'biometric_variance']
    X = df[features]
    y = df['is_fraud']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    model = XGBClassifier(n_estimators=120, max_depth=5, learning_rate=0.1, random_state=42)
    model.fit(X_train, y_train)
    
    preds = model.predict(X_test)
    auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
    recall = recall_score(y_test, preds)
    
    return model, df, auc, recall