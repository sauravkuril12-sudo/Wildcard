from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

FEATURES = [
	'amount', 'device_trust_score', 'velocity_1h', 'biometric_variance',
	'hour_of_day', 'merchant_history_count', 'location_change',
]
RANDOM_STATE = 42


def _evaluate(model, X_test, y_test):
	predictions = model.predict(X_test)
	probabilities = model.predict_proba(X_test)[:, 1]
	negatives = (y_test == 0).sum()
	positives = (y_test == 1).sum()
	false_positives = ((predictions == 1) & (y_test == 0)).sum()
	false_negatives = ((predictions == 0) & (y_test == 1)).sum()
	roc_auc = roc_auc_score(y_test, probabilities) if y_test.nunique() > 1 else None
	return {
		'Accuracy': accuracy_score(y_test, predictions),
		'Precision': precision_score(y_test, predictions, zero_division=0),
		'Recall': recall_score(y_test, predictions, zero_division=0),
		'ROC-AUC': roc_auc,
		'False positives': int(false_positives),
		'False negatives': int(false_negatives),
		'False-positive rate': false_positives / negatives if negatives else None,
		'False-negative rate': false_negatives / positives if positives else None,
	}


def run_closed_loop(data_path=None, mutation_count=500):
	"""Train Gen-1, mutate its missed fraud, and evaluate a held-out Gen-2 challenge."""
	if data_path is None:
		data_path = Path(__file__).resolve().parent / 'master_payment_simulation.csv'

	df = pd.read_csv(data_path)
	X = df[FEATURES]
	y = df['is_fraud']
	X_train, X_test, y_train, y_test = train_test_split(
		X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
	)

	# Gen-1 is intentionally capacity-limited so the red team can find misses.
	model_v1 = XGBClassifier(
		n_estimators=10, max_depth=2, learning_rate=0.1, random_state=RANDOM_STATE
	)
	model_v1.fit(X_train, y_train)
	baseline_metrics = _evaluate(model_v1, X_test, y_test)

	missed_mask = (model_v1.predict(X_test) == 0) & (y_test == 1)
	missed_attacks = X_test.loc[missed_mask].copy()
	if missed_attacks.empty:
		raise RuntimeError('Gen-1 produced no false negatives for the adaptation loop.')

	rng = np.random.default_rng(RANDOM_STATE)
	mutations = missed_attacks.sample(
		n=mutation_count, replace=True, random_state=RANDOM_STATE
	).copy()
	mutations['amount'] = np.maximum(
		0.01, mutations['amount'] * rng.uniform(0.9, 1.1, mutation_count)
	)
	mutations['velocity_1h'] = np.maximum(
		1, np.rint(mutations['velocity_1h'] + rng.integers(-2, 3, mutation_count))
	)
	mutations['biometric_variance'] = np.clip(
		mutations['biometric_variance'] + rng.normal(0, 0.002, mutation_count),
		0.0001,
		0.08,
	)
	mutations['is_fraud'] = 1
	mutations['fraud_vector'] = 'Gen2_Adaptive_Mutation'

	split_at = int(mutation_count * 0.8)
	mutation_train = mutations.iloc[:split_at]
	mutation_test = mutations.iloc[split_at:]
	X_hardened = pd.concat([X_train, mutation_train[FEATURES]], ignore_index=True)
	y_hardened = pd.concat([y_train, mutation_train['is_fraud']], ignore_index=True)

	model_v2 = XGBClassifier(
		n_estimators=100, max_depth=5, learning_rate=0.05, random_state=RANDOM_STATE
	)
	model_v2.fit(X_hardened, y_hardened)
	hardened_metrics = _evaluate(model_v2, X_test, y_test)
	adaptive_metrics = _evaluate(model_v2, mutation_test[FEATURES], mutation_test['is_fraud'])

	return {
		'model_v1': model_v1,
		'model_v2': model_v2,
		'data': df,
		'baseline_metrics': baseline_metrics,
		'hardened_metrics': hardened_metrics,
		'adaptive_metrics': adaptive_metrics,
		'missed_attacks': len(missed_attacks),
		'mutation_count': mutation_count,
	}


if __name__ == '__main__':
	result = run_closed_loop()
	print('=== INITIALIZING MASTERCARD CLOSED-LOOP ADVERSARIAL ENGINE ===')
	print(f"\n[Red Team Intelligence]: Found {result['missed_attacks']} Gen-1 false negatives.")
	print(f"[Closed-Loop Feedback]: Generated {result['mutation_count']} mutations from those misses.")
	print('\nGen-1 metrics:', result['baseline_metrics'])
	print('Gen-2 metrics:', result['hardened_metrics'])
	print('Gen-2 adaptive challenge recall:', result['adaptive_metrics']['Recall'])
