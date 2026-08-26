import pandas as pd
import numpy as np
from pathlib import Path

DEFAULT_DATA_PATH = Path(__file__).parent / "data" / "master_payment_simulation.csv"


def generate_synthetic_fraud_data(num_samples=1500, output_path=DEFAULT_DATA_PATH):
    np.random.seed(42)
    
    # Generate baseline features
    amounts = np.random.exponential(scale=70.0, size=num_samples)
    trust_scores = np.random.beta(a=5, b=2, size=num_samples)
    velocities = np.random.poisson(lam=3, size=num_samples)
    biometric_variance = np.random.uniform(0.01, 0.05, size=num_samples)
    
    # Inject Red Team Attack Vectors (V1, V2, V3)
    vectors = []
    labels = []
    
    for i in range(num_samples):
        # V1: Micro-Siphoning (Low amount, high velocity)
        if amounts[i] < 15.0 and velocities[i] > 8:
            vectors.append("V1: Micro-Siphoning")
            labels.append(1)
        # V2: Biometric Mimicry (Unnaturally low variance)
        elif biometric_variance[i] < 0.015 and trust_scores[i] < 0.5:
            vectors.append("V2: Biometric Mimicry")
            labels.append(1)
        # V3: Device Trust Evasion (Low trust score, high amount)
        elif trust_scores[i] < 0.25 and amounts[i] > 200:
            vectors.append("V3: Device Evasion")
            labels.append(1)
        else:
            # Normal legitimate behavior or random noise
            is_fraud = 1 if np.random.rand() < 0.08 else 0
            vectors.append("None" if is_fraud == 0 else "V1: General Fraud")
            labels.append(is_fraud)

    df = pd.DataFrame({
        'transaction_id': [f"TXN-{100000 + i}" for i in range(num_samples)],
        'user_id': [f"USR-{np.random.randint(1000, 5000)}" for i in range(num_samples)],
        'amount': np.round(amounts, 2),
        'device_trust_score': np.round(trust_scores, 4),
        'velocity_1h': velocities,
        'biometric_variance': np.round(biometric_variance, 4),
        'fraud_vector': vectors,
        'is_fraud': labels
    })
    
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return df

if __name__ == "__main__":
    generate_synthetic_fraud_data()