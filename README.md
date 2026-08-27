# 🛡️ Mastercard AI Defense Lab

> **Closed-Loop GenAI Payment Fraud Defense Engine**  
> *"Don’t just detect fraud. Learn from the fraud that beats you."*

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://wildcard-mscg.streamlit.app/)

🔗 **Live Interactive Demo:** [https://wildcard-mscg.streamlit.app/](https://wildcard-mscg.streamlit.app/)

The **Mastercard AI Defense Lab** is an interactive payment security system designed to detect, explain, and mitigate emerging GenAI-driven payment fraud vectors. By combining synthetic adversarial telemetry, structural firewall validation, explainable machine learning classification, and an adaptive closed-loop retraining pipeline, the platform bridges the gap between raw ML predictions and actionable enterprise fraud defense.

---

## 📌 Architecture Overview


[ Synthetic Payment Telemetry ]
(Amount, Device Score, Velocity, Variance)
│
▼
[ Fidelity Firewall ]
(Structural Integrity & Sanity Check)
│
▼
[ Defender ML Engine ]
(Gen-1 Baseline vs. Gen-2 Hardened)
│
▼
[ Explainable AI (XAI) Telemetry ]
(Attack Vector Matching: V1 / V2 / V3)
│
▼
[ Enterprise Decision Engine ]
(ALLOW ➔ STEP-UP ➔ REVIEW ➔ BLOCK)
│
▼
[ Adversarial Learning Loop ]
(Retrain on Missed Fraud / False Negatives)

---

## 🚀 Key Features

* **Live Threat Simulator**: Dynamically test payment telemetry inputs (Transaction Amount, Device Trust Score, 1-Hour Velocity, and Biometric Variance) in real-time.
* **Gen-1 vs. Gen-2 Hardening**: Toggle between baseline XGBoost defense and an adversarial-hardened model retrained on synthetic false negatives.
* **Fidelity Firewall**: Validates structural consistency and bounds of incoming transaction payloads before ML scoring.
* **Explainable AI (XAI) Alerts**: Breaks down why a transaction is flagged, linking anomalies directly to GenAI attack patterns.
* **Enterprise Decision Engine**: Automatically maps continuous risk scores ($0.00 \to 1.00$) into discrete operational actions:
  * `ALLOW` ($< 0.30$)
  * `STEP-UP` ($0.30 \le \text{Risk} < 0.60$)
  * `REVIEW` ($0.60 \le \text{Risk} < 0.85$)
  * `BLOCK` ($\ge 0.85$)
* **Inspection Audit History**: Log evaluation results to a local SQLite database for auditing and historical reviews.

---

## 🎯 Simulated GenAI Threat Vectors

| Vector | Name | Characteristics | Evasion Strategy |
| :--- | :--- | :--- | :--- |
| **V1** | **Agentic Micro-Siphoning** | High-velocity, ultra-low value ($<\$10$) transfers | Bypasses traditional static value thresholds |
| **V2** | **Behavioral Biometric Mimicry** | Robotic, near-zero biometric variance ($<0.05$) | Imitates human touch/typing patterns with synthetic precision |
| **V3** | **Context-Aware P2P Social Engineering** | High-value transfers initiated from trusted devices | Exploits high endpoint trust via deepfake/phishing coercion |

---

## 📂 Project Structure

```text
Wildcard/
├── apps/
│   └── streamlit/
│       ├── app.py                     # Streamlit UI & dashboard logic
│       ├── data_generator.py          # Synthetic payment telemetry generation
│       ├── defender_model.py          # XGBoost training & evaluation pipeline
│       ├── closed_loop.py             # Firewall validation & decision engine
│       ├── threat_profile.json        # Threat vector definitions & thresholds
│       ├── requirements.txt           # Python dependencies
│       ├── README.md                  # App-level documentation
│       └── data/
│           ├── master_payment_simulation.csv  # Generated simulation dataset
│           └── inspection_history.db          # SQLite audit log storage
├── README.md                          # Main repository documentation
└── .gitignore

🛠️ Local Installation & Setup
If you prefer to run the project locally instead of accessing the live hosted version:
1. Clone the Repository
git clone [https://github.com/sauravkuril12-sudo/Wildcard.git](https://github.com/sauravkuril12-sudo/Wildcard.git)
cd Wildcard

2. Set Up a Virtual Environment
Windows:
python -m venv .venv
.\.venv\Scripts\activate

macOS / Linux:
python3 -m venv .venv
source .venv/bin/activate

3. Install Dependencies
pip install -r apps/streamlit/requirements.txt

▶️ Running the Application Locally
Always launch the application from the repository root using streamlit run:
streamlit run apps/streamlit/app.py

For Windows environments specifying port and host explicitly:
.\.venv\Scripts\python.exe -m streamlit run apps/streamlit/app.py --server.address 0.0.0.0 --server.port 8501

Access the local server at http://localhost:8501/.
📦 Tech Stack
 * Frontend / UI: Streamlit
 * Machine Learning: XGBoost, scikit-learn
 * Data Processing: NumPy, Pandas
 * Storage / Persistence: SQLite

