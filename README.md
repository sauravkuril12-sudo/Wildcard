# 🛡️ Mastercard AI Defense Lab

> **Closed-Loop GenAI Payment Fraud Defense Engine**  
> *"Don’t just detect fraud. Learn from the fraud that beats you."*

[![Render](https://img.shields.io/badge/Render-Live_Demo-46E3B7?logo=render&logoColor=white)](https://wildcard-ervr.onrender.com)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://wildcard-mscg.streamlit.app/)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-181717?logo=github)](https://github.com/sauravkuril12-sudo/Wildcard)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)

* 🔗 **Primary Live Demo (Render):** [https://wildcard-ervr.onrender.com](https://wildcard-ervr.onrender.com)
* 🔗 **Backup Mirror (Streamlit Cloud):** [https://wildcard-mscg.streamlit.app/](https://wildcard-mscg.streamlit.app/)

The **Mastercard AI Defense Lab** is an interactive payment-security platform engineered to detect, explain, and mitigate emerging **GenAI-powered financial fraud vectors**. By integrating synthetic adversarial telemetry, structural fidelity firewall checks, explainable ML scoring, and an adaptive closed-loop retraining pipeline, the platform provides actionable enterprise defense against automated and synthetic threats.

---

## 📌 Architecture Overview

> **Data Pipeline:** `Synthetic Telemetry` ➔ `Fidelity Firewall` ➔ `ML Classifier` ➔ `Explainable AI` ➔ `Enterprise Verdict` ➔ `Feedback Loop`

| Stage | Component | Core Function |
| :---: | :--- | :--- |
| **01** | **Synthetic Payment Telemetry** | Simulates `Amount`, `Device Score`, `Velocity`, and `Biometric Variance`. |
| **02** | **Fidelity Firewall** | Enforces structural integrity and payload boundaries prior to ML inference. |
| **03** | **Defender ML Engine** | **XGBoost** scoring engine (`Gen-1 Baseline` vs. `Gen-2 Hardened`). |
| **04** | **Explainable AI (XAI)** | Detects telemetry anomalies matching attack vectors (**V1**, **V2**, **V3**). |
| **05** | **Enterprise Decision Engine** | Dispatches real-time verdicts: `ALLOW` \| `STEP-UP` \| `REVIEW` \| `BLOCK`. |
| **06** | **Adversarial Learning Loop** | Extracts False Negatives, mutates attack vectors, and retrains the defender. |

---

## 🎯 Simulated GenAI Threat Vectors

| Vector | Name | Characteristics | Evasion Strategy |
| :--- | :--- | :--- | :--- |
| **V1** | **Agentic Micro-Siphoning** | High-velocity, ultra-low value ($<\$10$) transfers | Bypasses traditional static transaction thresholds |
| **V2** | **Behavioral Biometric Mimicry** | Robotic, near-zero biometric variance ($<0.05$) | Imitates human touch/typing patterns with synthetic precision |
| **V3** | **Context-Aware P2P Social Engineering** | High-value transfers initiated from trusted devices | Exploits authenticated sessions via deepfake/phishing coercion |

---

## ⚙️ Enterprise Decision Engine

Continuous ML risk scores ($0.00 \to 1.00$) are mapped into discrete operational actions:

* **`ALLOW` ($< 0.30$)**: Frictionless path for low-risk, authentic user sessions.
* **`STEP-UP` ($0.30 \le \text{Risk} < 0.60$)**: Prompts for multi-factor authentication (MFA/Biometrics).
* **`REVIEW` ($0.60 \le \text{Risk} < 0.85$)**: Routes to the fraud operations queue for manual analyst review.
* **`BLOCK` ($\ge 0.85$)**: Immediate transaction termination and threat profiling.

---

## 🚀 Key Features

* **Live Threat Simulator**: Test custom telemetry values (Amount, Device Trust, Velocity, Biometric Variance) in real-time.
* **Gen-1 vs. Gen-2 Hardening**: Toggle between baseline XGBoost defense and an adversarial-hardened model retrained on synthetic false negatives.
* **Explainable AI (XAI)**: Actionable telemetry alerts explaining the exact attributes triggering the security verdict.
* **Persistence & Audit History**: Log evaluations directly into a local SQLite database for historical compliance and audit review.

---

## 📂 Project Structure

```text
Wildcard/
├── apps/
│   └── streamlit/
│       ├── app.py                     # Streamlit frontend & dashboard UI
│       ├── data_generator.py          # Synthetic payment telemetry generation
│       ├── defender_model.py          # XGBoost model training & evaluation
│       ├── closed_loop.py             # Firewall validation & decision engine
│       ├── threat_profile.json        # GenAI threat vector specifications
│       ├── requirements.txt           # Python dependencies
│       ├── README.md                  # App-specific documentation
│       └── data/
│           ├── master_payment_simulation.csv  # Simulation dataset
│           └── inspection_history.db          # SQLite audit database
├── README.md                          # Repository documentation
└── .gitignore

🛠️ Local Installation & Setup
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

Windows explicit command:
.\.venv\Scripts\python.exe -m streamlit run apps/streamlit/app.py --server.address 0.0.0.0 --server.port 8501

Access the local server at http://localhost:8501/.
📦 Tech Stack
 * Frontend / UI: Streamlit
 * Machine Learning: XGBoost, scikit-learn
 * Data Processing: NumPy, Pandas
 * Database: SQLite
 * Deployment: Render, Streamlit Community Cloud

