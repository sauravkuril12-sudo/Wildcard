import streamlit as st
import pandas as pd
from pathlib import Path
from xgboost import DMatrix
from closed_loop import FEATURES, run_closed_loop

# Page Configuration with Mastercard Theme feel
st.set_page_config(
    page_title="Mastercard AI Defense Lab",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Modern Fintech UI Styling
st.markdown("""
    <style>
        .main {
            background-color: #0F172A;
            color: #F8FAFC;
        }
        .stSidebar {
            background-color: #1E293B;
        }
        h1, h2, h3 {
            color: #F8FAFC !important;
            font-family: 'Inter', sans-serif;
        }
        .metric-card {
            background-color: #1E293B;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #334155;
            text-align: center;
        }
        .stAlert {
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.title("🛡️ Mastercard AI Defense Lab")
st.markdown("### **Enterprise GenAI Payment Security & Closed-Loop Intelligence**")
st.markdown("---")

# Load data and train model behind the scenes (Backend)
@st.cache_resource
def load_and_train_model(feature_schema):
    data_path = Path(__file__).resolve().parent / 'master_payment_simulation.csv'
    loop_result = run_closed_loop(data_path)
    return loop_result['model_v2'], loop_result['data'], loop_result

model, df, loop_result = load_and_train_model(tuple(FEATURES))


def explain_prediction(model, user_input, probability):
    """Return local model contributions and a human-readable threat assessment."""
    booster = model.get_booster()
    contribution_frame = booster.predict(
        DMatrix(user_input[FEATURES]), pred_contribs=True
    )
    contributions = contribution_frame[0][:-1]
    strongest_index = max(range(len(FEATURES)), key=lambda index: abs(contributions[index]))
    strongest_feature = FEATURES[strongest_index]

    signal_labels = {
        'amount': 'Transaction amount',
        'device_trust_score': 'Device trust score',
        'velocity_1h': 'Transaction velocity',
        'biometric_variance': 'Biometric variance',
        'hour_of_day': 'Time of day',
        'merchant_history_count': 'Merchant history',
        'location_change': 'Location change',
    }
    baseline_text = {
        'amount': f"${df['amount'].median():.2f} median legitimate amount",
        'device_trust_score': f"{df['device_trust_score'].median():.2f} typical device trust",
        'velocity_1h': '1-3 transactions/hour normal baseline',
        'biometric_variance': f"{df['biometric_variance'].median():.3f} typical variance",
        'hour_of_day': 'daytime activity baseline',
        'merchant_history_count': f"{df['merchant_history_count'].median():.0f} prior merchant transactions",
        'location_change': 'no recent location change',
    }

    if user_input.at[0, 'amount'] <= 3.0 and user_input.at[0, 'velocity_1h'] >= 10:
        threat_vector = 'Agentic Micro-Siphoning'
        recommended_action = 'BLOCK and investigate account activity'
    elif user_input.at[0, 'biometric_variance'] <= 0.005 and user_input.at[0, 'device_trust_score'] >= 0.9:
        threat_vector = 'Behavioral Biometric Mimicry'
        recommended_action = 'STEP-UP authentication and verify device ownership'
    elif user_input.at[0, 'amount'] >= 500.0 and user_input.at[0, 'device_trust_score'] >= 0.95:
        threat_vector = 'Context-Aware P2P Social Engineering'
        recommended_action = 'HOLD for review and confirm transfer intent'
    elif probability >= 0.5:
        threat_vector = 'Unclassified elevated-risk behavior'
        recommended_action = 'HOLD for review'
    else:
        threat_vector = 'No known threat vector matched'
        recommended_action = 'ALLOW and continue monitoring'

    return {
        'feature': strongest_feature,
        'strongest_feature': signal_labels[strongest_feature],
        'contribution': contributions[strongest_index],
        'baseline': baseline_text[strongest_feature],
        'threat_vector': threat_vector,
        'recommended_action': recommended_action,
        'contributions': pd.DataFrame({
            'Signal': [signal_labels[feature] for feature in FEATURES],
            'Model contribution': contributions,
        }).sort_values('Model contribution', key=lambda values: values.abs(), ascending=False),
    }


def get_risk_decision(probability, block_threshold):
    if probability >= block_threshold:
        return 'BLOCK', 'Maximum fraud protection; may increase false declines.'
    if probability >= 0.50:
        return 'HOLD FOR REVIEW', 'Reduces fraud loss while routing borderline payments to an analyst.'
    if probability >= 0.25:
        return 'STEP-UP AUTHENTICATION', 'Adds customer friction, but can safely verify uncertain payments.'
    return 'ALLOW', 'Lowest customer friction; accepts more residual fraud exposure.'


def build_attack_profile(user_input, objective):
    attack = user_input.copy()
    if objective == 'Stay below amount thresholds':
        attack.loc[0, ['amount', 'velocity_1h', 'location_change']] = [2.50, max(12, attack.at[0, 'velocity_1h']), 1]
    elif objective == 'Mimic trusted biometrics':
        attack.loc[0, ['device_trust_score', 'biometric_variance', 'hour_of_day']] = [0.97, 0.003, 2]
    else:
        attack.loc[0, ['amount', 'device_trust_score', 'merchant_history_count', 'location_change']] = [850.0, 0.99, 1, 1]
    return attack

# Top Metrics Row
metrics = loop_result['hardened_metrics']
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Total Simulated Transactions", value=f"{len(df):,}")
with col2:
    st.metric(label="Blocked GenAI Frauds", value=f"{df['is_fraud'].sum():,}")
with col3:
    st.metric(label="Gen-2 ROC-AUC", value=f"{metrics['ROC-AUC']:.4f}")
with col4:
    st.metric(label="Precision", value=f"{metrics['Precision']:.2%}")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Recall", value=f"{metrics['Recall']:.2%}")
with col2:
    fpr = metrics.get('False-positive rate')
    fpr_display = f"{fpr:.2%}" if fpr is not None else "—"
    st.metric(label="False-Positive Rate", value=fpr_display)
with col3:
    fnr = metrics.get('False-negative rate')
    fnr_display = f"{fnr:.2%}" if fnr is not None else "—"
    st.metric(label="False-Negative Rate", value=fnr_display)
with col4:
    st.metric(label="Closed-Loop Status", value="Active / Hardened")

st.markdown("---")

# Closed-loop adaptation evidence
st.subheader("🔁 Closed-Loop Adaptation")
adapt_col1, adapt_col2, adapt_col3 = st.columns(3)
with adapt_col1:
    st.metric("Gen-1 Missed Attacks", f"{loop_result['missed_attacks']:,}")
with adapt_col2:
    st.metric("Gen-2 Mutations Generated", f"{loop_result['mutation_count']:,}")
with adapt_col3:
    recall_change = loop_result['hardened_metrics']['Recall'] - loop_result['baseline_metrics']['Recall']
    st.metric("Recall Improvement", f"{recall_change:+.2%}")

comparison = pd.DataFrame({
    'Metric': ['Accuracy', 'Precision', 'Recall', 'ROC-AUC'],
    'Gen-1': [loop_result['baseline_metrics'][metric] for metric in ['Accuracy', 'Precision', 'Recall', 'ROC-AUC']],
    'Gen-2': [loop_result['hardened_metrics'][metric] for metric in ['Accuracy', 'Precision', 'Recall', 'ROC-AUC']],
}).set_index('Metric')
st.bar_chart(comparison, y_label='Score', x_label='Defender generation')
st.caption(
    f"Red team found {loop_result['missed_attacks']} Gen-1 false negatives. "
    f"Gen-2 was retrained with {loop_result['mutation_count']} mutations and achieved "
    f"{loop_result['adaptive_metrics']['Recall']:.1%} recall on held-out adaptive attacks."
)

st.markdown("---")

# Sidebar Controls (Interactive Testing Panel)
st.sidebar.header("🕹️ Live Threat Simulator")
st.sidebar.markdown("Adjust transaction parameters to test the AI defense model in real-time:")
block_threshold = st.sidebar.number_input(
    "Block Risk Threshold",
    min_value=0.50,
    max_value=0.99,
    value=0.75,
    step=0.01,
    format="%.2f",
    help="Predictions at or above this probability are blocked.",
)
st.sidebar.caption(
    "Lower threshold: stronger fraud protection, more customer friction. "
    "Higher threshold: smoother payments, more residual fraud risk."
)

input_amount = st.sidebar.number_input(
    "Transaction Amount ($)",
    min_value=0.10,
    max_value=3000.0,
    value=45.0,
    step=0.01,
    format="%.2f",
    help="Enter the exact transaction amount to simulate micro-siphoning or high-value P2P transfer",
)
input_trust = st.sidebar.slider("Device Trust Score", 0.0, 1.0, 0.85, help="Lower scores indicate compromised devices")
input_velocity = st.sidebar.slider("1-Hour Transaction Velocity", 1, 30, 2, help="High velocity signals automated agent attacks")
input_biometric = st.sidebar.slider("Biometric Variance", 0.0001, 0.05, 0.04, help="Unnaturally low variance indicates robotic typing mimicry")
input_hour = st.sidebar.slider("Hour of Day", 0, 23, 12, help="Unusual hours can add context to the risk assessment")
input_history = st.sidebar.number_input("Merchant History Count", 0, 100, 8, help="Prior transactions with this merchant")
input_location_change = st.sidebar.checkbox("Recent Location Change", value=False)
attack_objective = st.sidebar.selectbox(
    "Red-Team Attack Objective",
    ['Stay below amount thresholds', 'Mimic trusted biometrics', 'Abuse a trusted device'],
    help="Choose how an attacker modifies the baseline transaction.",
)

# Main Evaluation Section
st.subheader("🔍 Real-Time Transaction Inspection")

user_input = pd.DataFrame([[
    input_amount, input_trust, input_velocity, input_biometric,
    input_hour, input_history, int(input_location_change),
]], columns=FEATURES)

prediction = model.predict(user_input)[0]
probability = model.predict_proba(user_input)[0][1]
explanation = explain_prediction(model, user_input, probability)
decision, decision_tradeoff = get_risk_decision(probability, block_threshold)
attack_input = build_attack_profile(user_input, attack_objective)
attack_probability = model.predict_proba(attack_input)[0][1]
attack_explanation = explain_prediction(model, attack_input, attack_probability)
attack_decision, attack_tradeoff = get_risk_decision(attack_probability, block_threshold)

res_col1, res_col2 = st.columns([1, 1])

with res_col1:
    st.markdown("#### Input Parameters Summary")
    st.dataframe(user_input.T, width='stretch')

with res_col2:
    st.markdown("#### AI Security Verdict")
    st.metric("Live Risk Score", f"{probability:.2%}")
    if decision == 'BLOCK':
        st.error(f"🚫 **DECISION: {decision}**\n\n* **Risk Probability:** `{probability*100:.2f}%`\n* **Threshold:** `{block_threshold:.2%}`")
    elif decision == 'HOLD FOR REVIEW':
        st.warning(f"⏸️ **DECISION: {decision}**\n\n* **Risk Probability:** `{probability*100:.2f}%`")
    elif decision == 'STEP-UP AUTHENTICATION':
        st.info(f"🔐 **DECISION: {decision}**\n\n* **Risk Probability:** `{probability*100:.2f}%`")
    else:
        st.success(f"✅ **DECISION: {decision}**\n\n* **Risk Probability:** `{probability*100:.2f}%`")
    st.markdown(f"**Matched Threat Vector:** {explanation['threat_vector']}")
    st.markdown(f"**Recommended Action:** {decision}")
    st.caption(f"Policy tradeoff: {decision_tradeoff}")

with res_col1:
    st.markdown(
        f"**Top Signal:** {explanation['strongest_feature']} contributed "
        f"{explanation['contribution']:+.3f} to the model score."
    )
    st.caption(
        f"Current value: {user_input.at[0, explanation['feature']]} | "
        f"Reference: {explanation['baseline']}"
    )
    st.dataframe(explanation['contributions'], hide_index=True, width='stretch')

st.markdown("---")

# Red-team attack canvas
st.subheader("🎯 Red-Team Attack Canvas")
st.caption(
    f"Objective: **{attack_objective}**. The attacker modifies the baseline transaction, "
    "then the defender evaluates the mutated profile."
)
changes = pd.DataFrame({
    'Signal': FEATURES,
    'Baseline': [user_input.at[0, feature] for feature in FEATURES],
    'Attacker value': [attack_input.at[0, feature] for feature in FEATURES],
})
changes['Change'] = changes['Attacker value'] - changes['Baseline']
st.dataframe(changes, hide_index=True, width='stretch')

canvas_col1, canvas_col2 = st.columns(2)
with canvas_col1:
    st.metric("Attack Risk Score", f"{attack_probability:.2%}")
    st.markdown(f"**Top signal:** {attack_explanation['strongest_feature']}")
    st.markdown(f"**Matched vector:** {attack_explanation['threat_vector']}")
with canvas_col2:
    if attack_decision == 'BLOCK':
        st.error(f"**DEFENDER RESPONSE: {attack_decision}**")
    elif attack_decision == 'HOLD FOR REVIEW':
        st.warning(f"**DEFENDER RESPONSE: {attack_decision}**")
    elif attack_decision == 'STEP-UP AUTHENTICATION':
        st.info(f"**DEFENDER RESPONSE: {attack_decision}**")
    else:
        st.success(f"**DEFENDER RESPONSE: {attack_decision}**")
    st.caption(attack_tradeoff)

st.markdown("---")

# Dataset Preview Section
st.subheader("📊 Master Simulation Dataset Preview")
st.markdown("A sample of the 20,000 synthetic transaction records generated via our Red Team threat profile engine:")
st.dataframe(df[['transaction_id', 'user_id', 'amount', 'merchant_category', 'fraud_vector', 'is_fraud']].head(10), width='stretch')
