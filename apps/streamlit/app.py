import streamlit as st
import pandas as pd
from pathlib import Path
from data_generator import generate_synthetic_fraud_data
from defender_model import train_defender_model
from closed_loop import fidelity_firewall, evaluate_enterprise_decision
import json
import sqlite3
from datetime import datetime

APP_DIR = Path(__file__).parent
DATA_PATH = APP_DIR / "data" / "master_payment_simulation.csv"
DB_PATH = APP_DIR / "data" / "inspection_history.db"
PROFILE_PATH = APP_DIR / "threat_profile.json"

st.set_page_config(
    page_title="Mastercard AI Defense Lab",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');
    :root { --red:#eb001b; --orange:#ff5f00; --yellow:#ffb600; --bg:#0e1117; --card:#161b22; --border:#30363d; --muted:#6e7681; --secondary:#8b949e; --text:#f0f6fc; --green:#3fb950; }
    html, body, [class*="css"] { font-family:'Inter', sans-serif; }
    .stApp { background:radial-gradient(ellipse at top left,rgba(235,0,27,.06),transparent 45%),radial-gradient(ellipse at bottom right,rgba(255,95,0,.04),transparent 45%),var(--bg); color:var(--text); }
    [data-testid="stHeader"] { background:rgba(14,17,23,.88); } [data-testid="stToolbar"] { visibility:hidden; }
    .block-container { max-width:1440px; padding:1.5rem 2rem 4rem; }
    h1,h2,h3 { font-family:'Space Grotesk',sans-serif !important; color:var(--text) !important; } h1{font-size:1.55rem !important;margin:0 !important;} h2{font-size:1.15rem !important;margin:0 0 1rem !important;}
    p,label,.stCaption { color:var(--secondary) !important; }
    .topbar{display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid var(--border);padding:0 0 1.3rem;margin-bottom:1.4rem}.brand{display:flex;align-items:center;gap:14px}.brand-mark{width:46px;height:46px;display:grid;place-items:center;border-radius:12px;background:linear-gradient(135deg,var(--orange),var(--red));box-shadow:0 4px 20px rgba(235,0,27,.24);font-size:24px}.subtitle{color:var(--muted);font-size:.72rem;letter-spacing:.04em;margin-top:3px}.engine{color:var(--green);font-size:.78rem;font-weight:600;display:flex;align-items:center;gap:7px}.live-dot{width:8px;height:8px;background:var(--green);border-radius:50%;display:inline-block;box-shadow:0 0 9px var(--green)}.mode{border:1px solid var(--border);border-radius:8px;padding:7px 11px;color:var(--secondary);font-size:.7rem;font-weight:700;letter-spacing:.06em}
    .metric,.panel,.vector{background:var(--card);border:1px solid var(--border);border-radius:14px}.metric{padding:1rem 1.1rem .85rem;min-height:92px}.metric-label,.eyebrow{color:var(--muted);font-size:.68rem;text-transform:uppercase;letter-spacing:.07em;font-weight:600}.metric-value{font-family:'Space Grotesk',sans-serif;color:var(--text);font-size:1.45rem;font-weight:700;margin-top:.35rem}.metric-status{font-size:1.15rem;white-space:nowrap}.panel{padding:1.35rem;min-height:100%}.panel-title{font-family:'Space Grotesk',sans-serif;color:var(--text);font-weight:600;font-size:1rem;margin-bottom:1.1rem}.section{margin-top:2.5rem}.decision{border:1px solid;border-radius:12px;padding:1.15rem;margin:.9rem 0 1rem}.decision-name{font-family:'Space Grotesk',sans-serif;font-size:1.6rem;font-weight:700}.risk-track{background:var(--border);height:8px;border-radius:4px;overflow:hidden;margin-top:.45rem}.risk-fill{height:100%;background:linear-gradient(90deg,var(--green),var(--yellow),var(--orange),var(--red));border-radius:4px}.alert{border:1px solid rgba(235,0,27,.25);background:rgba(235,0,27,.09);border-radius:9px;padding:.65rem .75rem;margin:.4rem 0;font-size:.8rem;color:var(--secondary)}.normal{border-color:rgba(46,160,67,.25);background:rgba(46,160,67,.07);color:var(--green)}
    .vector{padding:1.2rem;min-height:230px;border-top:3px solid var(--orange)}.vector-code{color:var(--orange);font-size:.7rem;font-weight:700;letter-spacing:.08em}.vector-name{font-family:'Space Grotesk',sans-serif;color:var(--text);font-size:1rem;font-weight:600;margin:.25rem 0 .7rem}.vector-copy{color:var(--secondary);font-size:.8rem;line-height:1.55;min-height:55px}.bypass{border-top:1px solid var(--border);padding-top:.7rem;margin-top:.9rem;color:var(--secondary);font-size:.75rem;line-height:1.5}.bypass strong{color:var(--muted);display:block;text-transform:uppercase;font-size:.65rem;letter-spacing:.07em;margin-bottom:.25rem}.history-row{display:flex;align-items:center;justify-content:space-between;gap:1rem;flex-wrap:wrap;background:rgba(255,255,255,.02);border:1px solid var(--border);border-radius:9px;padding:.75rem 1rem;margin:.45rem 0}.history-item{color:var(--secondary);font-size:.78rem}.history-item strong{color:var(--text);margin-left:.25rem}.stButton>button{border:1px solid var(--border);background:transparent;color:var(--secondary);border-radius:8px;font-weight:600}.stButton>button:hover{border-color:var(--orange);color:var(--text)}
    [data-testid="stVerticalBlockBorderWrapper"]{background:var(--card);border-color:var(--border);border-radius:14px;padding:1.1rem 1.25rem} div[data-baseweb="input"]>div,div[data-baseweb="select"]>div{background:var(--bg);border-color:var(--border)} [data-testid="stDataFrame"]{border:1px solid var(--border);border-radius:10px;overflow:hidden}
    </style>
    """,
    unsafe_allow_html=True,
)

def init_database():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS inspection_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                trust REAL NOT NULL,
                velocity INTEGER NOT NULL,
                variance REAL NOT NULL,
                risk_score REAL NOT NULL,
                decision TEXT NOT NULL,
                firewall_passed INTEGER NOT NULL,
                firewall_message TEXT NOT NULL,
                alerts TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )

def save_inspection(amount, trust, velocity, variance, risk_score, decision, passed, message, alerts):
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            "INSERT INTO inspection_logs (amount, trust, velocity, variance, risk_score, decision, firewall_passed, firewall_message, alerts, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (amount, trust, velocity, variance, risk_score, decision, int(passed), message, json.dumps(alerts), datetime.now().isoformat(timespec="seconds")),
        )

def load_inspections():
    with sqlite3.connect(DB_PATH) as connection:
        return connection.execute(
            "SELECT amount, trust, velocity, variance, risk_score, decision, firewall_passed, created_at FROM inspection_logs ORDER BY id DESC LIMIT 20"
        ).fetchall()

init_database()
if not DATA_PATH.exists():
    generate_synthetic_fraud_data(output_path=DATA_PATH)

profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
mutation_active = st.session_state.get("mutation_active", False)
model, df, auc, recall = train_defender_model(
    csv_path=DATA_PATH, mutation_boost=mutation_active
)

st.markdown(
    f'<div class="topbar"><div class="brand"><div class="brand-mark">🛡</div><div><h1>Mastercard AI Defense Lab</h1><div class="subtitle">Enterprise GenAI Payment Security &amp; Closed-Loop Intelligence</div></div></div><div style="display:flex;align-items:center;gap:18px"><div class="engine"><span class="live-dot"></span>Engine Online</div><div class="mode">GEN-{2 if mutation_active else 1} {"HARDENED" if mutation_active else "BASELINE"}</div></div></div>',
    unsafe_allow_html=True,
)

metric_columns = st.columns(4)
metrics = [
    ("Simulated Transactions", f"{len(df):,}+"),
    ("Blocked GenAI Frauds", f"{int(df['is_fraud'].sum()):,}"),
    ("Defender Accuracy (ROC-AUC)", f"{auc:.4f}"),
    ("Closed-Loop Status", "Active / Hardened" if mutation_active else "Active / Baseline"),
]
for column, (label, value) in zip(metric_columns, metrics):
    with column:
        status_class = " metric-status" if label == "Closed-Loop Status" else ""
        st.markdown(f'<div class="metric"><div class="metric-label">{label}</div><div class="metric-value{status_class}">{value}</div></div>', unsafe_allow_html=True)

st.markdown('<div class="section"></div>', unsafe_allow_html=True)
simulator, verdict = st.columns([0.9, 1.35], gap="large")
with simulator:
    with st.container(border=True):
        st.markdown('<div class="panel-title">⚡ Live Threat Simulator</div><div class="subtitle" style="margin-bottom:1rem">Adjust telemetry parameters to simulate adversarial transaction patterns</div>', unsafe_allow_html=True)
        amount = st.number_input("Transaction Amount", min_value=0.10, max_value=3000.00, value=45.00, step=0.10, format="%.2f", help="Type any exact amount to test micro-siphoning detection")
        trust = st.slider("Device Trust Score", 0.0, 1.0, 0.85, 0.01, format="%.2f")
        velocity = st.slider("1-Hour Velocity", 1, 30, 2, 1, format="%d txns")
        variance = st.slider("Biometric Variance", 0.001, 0.050, 0.035, 0.001, format="%.3f")
        mutation_active = st.toggle(
            "Gen-2 Mutation Hardening",
            value=st.session_state.get("mutation_active", False),
            key="mutation_active",
            help="Switch between the Gen-1 baseline model and the Gen-2 adversarially hardened model.",
        )
        st.markdown(
            f'<div class="subtitle">Current model: GEN-{2 if mutation_active else 1} {"HARDENED" if mutation_active else "BASELINE"}</div>',
            unsafe_allow_html=True,
        )

with verdict:
    passed, firewall_message = fidelity_firewall(amount, trust, velocity, variance)
    probability = float(model.predict_proba(pd.DataFrame([[amount, trust, velocity, variance]], columns=["amount", "device_trust_score", "velocity_1h", "biometric_variance"]))[0][1]) if passed else 0.0
    decision, description = evaluate_enterprise_decision(probability) if passed else ("BLOCK", firewall_message)
    alerts = []
    if velocity > 8:
        alerts.append("High velocity spike matches V1 Micro-Siphoning signature.")
    if variance < 0.015:
        alerts.append("Low variance matches V2 Robotic Biometric Mimicry.")
    if trust < 0.3:
        alerts.append("Low trust score matches V3 Compromised Endpoint Evasion.")
    if not alerts and passed:
        alerts.append("Telemetry Normal: Behavioral biometrics align with standard user patterns.")
    colors = {"ALLOW": ("#3fb950", "rgba(46,160,67,.08)"), "STEP-UP": ("#ffb600", "rgba(255,182,0,.08)"), "REVIEW": ("#d29922", "rgba(210,153,34,.08)"), "BLOCK": ("#eb001b", "rgba(235,0,27,.12)")}
    color, background = colors[decision]
    with st.container(border=True):
        st.markdown('<div class="panel-title">🛡 Enterprise Security Verdict</div>', unsafe_allow_html=True)
        firewall_color = "#3fb950" if passed else "#eb001b"
        st.markdown(f'<div style="border:1px solid {firewall_color};background:{background};border-radius:9px;padding:.65rem .8rem;color:{firewall_color};font-size:.8rem">{"✓" if passed else "×"} Fidelity Firewall: {firewall_message}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="decision" style="border-color:{color};background:{background}"><div class="eyebrow">Decision</div><div class="decision-name" style="color:{color}">{decision}</div><p style="margin:.5rem 0 1rem">{description}</p><div class="risk-track"><div class="risk-fill" style="width:{probability * 100:.2f}%"></div></div></div>', unsafe_allow_html=True)
        st.markdown('<div class="eyebrow">Explainable AI Telemetry Breakdown</div>', unsafe_allow_html=True)
        for alert in alerts:
            st.markdown(f'<div class="alert {"normal" if alert.startswith("Telemetry Normal") else ""}">{alert}</div>', unsafe_allow_html=True)
        if st.button("▣ Log Inspection to Database", width="stretch"):
            save_inspection(amount, trust, velocity, variance, probability, decision, passed, firewall_message, alerts)
            st.success("Inspection logged successfully.")

st.markdown('<div class="section"></div>', unsafe_allow_html=True)
st.markdown("## GenAI Threat Vectors")
vector_columns = st.columns(3, gap="large")
vector_colors = {"V1": "#ff5f00", "V2": "#ffb600", "V3": "#eb001b"}
for column, vector in zip(vector_columns, profile["fraud_vectors"]):
    with column:
        vector_color = vector_colors.get(vector["vector_id"], "#ff5f00")
        st.markdown(f'<div class="vector" style="border-top-color:{vector_color}"><div class="vector-code">{vector["vector_id"]}</div><div class="vector-name">{vector["name"]}</div><div class="vector-copy">{vector["description"]}</div><div class="bypass"><strong>Bypass Mechanism</strong>{vector["parameters"]["primary_bypass_mechanism"]}</div></div>', unsafe_allow_html=True)

st.markdown('<div class="section"></div>', unsafe_allow_html=True)
st.markdown("## Master Simulation Dataset")
display_data = df[["transaction_id", "user_id", "amount", "device_trust_score", "velocity_1h", "fraud_vector", "is_fraud"]].head(10).copy()
display_data["amount"] = display_data["amount"].map(lambda value: f"Rs {value:.2f}")
display_data["device_trust_score"] = display_data["device_trust_score"].map(lambda value: f"{value:.4f}")
display_data["is_fraud"] = display_data["is_fraud"].map({0: "Legit", 1: "Fraud"})
display_data.columns = ["Transaction ID", "User ID", "Amount", "Trust Score", "Velocity", "Fraud Vector", "Status"]
st.dataframe(display_data, width="stretch", hide_index=True)

st.markdown('<div class="section"></div>', unsafe_allow_html=True)
history_header, refresh_column = st.columns([4, 1])
with history_header:
    st.markdown("## Inspection History")
with refresh_column:
    if st.button("↻ Refresh", width="stretch"):
        st.rerun()

history = load_inspections()
if not history:
    st.markdown('<div class="panel" style="text-align:center;color:#6e7681">No inspections logged yet. Click “Log Inspection to Database” to record a transaction.</div>', unsafe_allow_html=True)
else:
    for row in history:
        amount_value, trust_value, velocity_value, variance_value, risk_value, decision_value, firewall_passed, created_at = row
        decision_color = colors.get(decision_value, ("#eb001b", ""))[0]
        time_value = datetime.fromisoformat(created_at).strftime("%I:%M:%S %p")
        rejected = '<span style="color:#eb001b;font-size:.7rem">Firewall Rejected</span>' if not firewall_passed else ""
        st.markdown(
            f'<div class="history-row"><div style="display:flex;gap:1.5rem;flex-wrap:wrap"><span class="history-item">Amount<strong>Rs {amount_value:.2f}</strong></span><span class="history-item">Trust<strong>{trust_value:.2f}</strong></span><span class="history-item">Velocity<strong>{velocity_value}</strong></span><span class="history-item">Risk<strong style="color:{decision_color}">{risk_value * 100:.1f}%</strong></span></div><div style="display:flex;align-items:center;gap:1rem">{rejected}<strong style="color:{decision_color}">{decision_value}</strong><span style="color:#6e7681;font-size:.7rem">{time_value}</span></div></div>',
            unsafe_allow_html=True,
        )