import json
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

with open(Path(__file__).resolve().parent / 'threat_profile.json', 'r') as f:
    threat_profile = json.load(f)

print(f"Loaded Profile: {threat_profile['challenge']} - {threat_profile['lab']}")

def generate_payment_simulation(num_records=20000, fraud_ratio=0.06):
    rng = np.random.default_rng(42)
    user_pool = [f"usr_{i:04d}" for i in range(1500)]
    user_activity = rng.gamma(shape=2.0, scale=1.0, size=len(user_pool))
    user_trust = rng.beta(8, 2, size=len(user_pool))
    user_home_region = rng.integers(0, 8, size=len(user_pool))
    user_index = rng.choice(len(user_pool), num_records, p=user_activity / user_activity.sum())
    hour_weights = np.array([
        0.015, 0.01, 0.008, 0.008, 0.01, 0.015, 0.025, 0.04,
        0.065, 0.075, 0.07, 0.065, 0.06, 0.06, 0.06, 0.065,
        0.07, 0.075, 0.07, 0.055, 0.04, 0.03, 0.02, 0.014,
    ])
    hours = rng.choice(np.arange(24), num_records, p=hour_weights / hour_weights.sum())
    timestamps = [
        datetime.now().replace(hour=int(hour), minute=int(rng.integers(0, 60)), second=0, microsecond=0)
        - timedelta(days=int(rng.integers(0, 100)))
        for hour in hours
    ]
    merchant_categories = ['grocery', 'retail', 'dining', 'subscription', 'p2p_transfer']
    merchants = rng.choice(merchant_categories[:-1], num_records)
    user_history = rng.poisson(8, num_records)
    location_change = rng.binomial(1, 0.04, num_records)
    device_trust = np.clip(user_trust[user_index] + rng.normal(0, 0.08, num_records), 0.05, 1.0)
    
    df = pd.DataFrame({
        'transaction_id': [f"tx_{i:06d}" for i in range(num_records)],
        'timestamp': timestamps,
        'user_id': [user_pool[index] for index in user_index],
        'amount': np.clip(rng.lognormal(np.log(38), 0.85, num_records), 0.10, 3000.0),
        'device_trust_score': device_trust,
        'velocity_1h': rng.poisson(1.5 + user_activity[user_index] * 0.3, num_records),
        'biometric_variance': np.clip(rng.normal(0.038, 0.012, num_records), 0.0005, 0.08),
        'hour_of_day': hours,
        'merchant_history_count': user_history,
        'location_change': location_change,
        'merchant_category': merchants,
        'is_fraud': 0,
        'fraud_vector': 'None'
    })

    num_fraud = int(num_records * fraud_ratio)
    fraud_indices = rng.choice(num_records, num_fraud, replace=False)
    chunk = num_fraud // 3
    
    v1_idx = fraud_indices[:chunk]
    v2_idx = fraud_indices[chunk:2*chunk]
    v3_idx = fraud_indices[2*chunk:]
    
    df.loc[v1_idx, 'amount'] = np.clip(rng.lognormal(np.log(4.0), 0.65, len(v1_idx)), 0.50, 18.0)
    df.loc[v1_idx, 'velocity_1h'] = rng.poisson(lam=10, size=len(v1_idx))
    df.loc[v1_idx, 'location_change'] = rng.binomial(1, 0.25, len(v1_idx))
    df.loc[v1_idx, 'is_fraud'] = 1
    df.loc[v1_idx, 'fraud_vector'] = 'Agentic_Micro_Siphoning'
    
    df.loc[v2_idx, 'amount'] = np.clip(rng.lognormal(np.log(100), 0.65, len(v2_idx)), 20.0, 500.0)
    df.loc[v2_idx, 'device_trust_score'] = np.clip(rng.normal(0.88, 0.09, len(v2_idx)), 0.40, 1.0)
    df.loc[v2_idx, 'biometric_variance'] = np.clip(rng.normal(0.012, 0.006, len(v2_idx)), 0.001, 0.05)
    df.loc[v2_idx, 'hour_of_day'] = rng.choice([0, 1, 2, 3, 22, 23], len(v2_idx))
    df.loc[v2_idx, 'is_fraud'] = 1
    df.loc[v2_idx, 'fraud_vector'] = 'Behavioral_Biometric_Mimicry'
    
    df.loc[v3_idx, 'amount'] = np.clip(rng.lognormal(np.log(800), 0.7, len(v3_idx)), 250.0, 3000.0)
    df.loc[v3_idx, 'device_trust_score'] = np.clip(rng.normal(0.93, 0.06, len(v3_idx)), 0.60, 1.0)
    df.loc[v3_idx, 'velocity_1h'] = rng.poisson(2.5, len(v3_idx))
    df.loc[v3_idx, 'location_change'] = rng.binomial(1, 0.55, len(v3_idx))
    df.loc[v3_idx, 'merchant_category'] = 'p2p_transfer'
    df.loc[v3_idx, 'is_fraud'] = 1
    df.loc[v3_idx, 'fraud_vector'] = 'P2P_Social_Engineering'

    noise_count = max(1, int(num_records * 0.01))
    noisy_indices = rng.choice(num_records, noise_count, replace=False)
    df.loc[noisy_indices, 'is_fraud'] = 1 - df.loc[noisy_indices, 'is_fraud']
    df.loc[noisy_indices, 'fraud_vector'] = 'Label_Noise'
    return df

df_master = generate_payment_simulation()
df_master.to_csv(Path(__file__).resolve().parent / 'master_payment_simulation.csv', index=False)
print(f"Successfully generated {len(df_master)} transactions!")
print("Fraud Breakdown:")
print(df_master['fraud_vector'].value_counts())
