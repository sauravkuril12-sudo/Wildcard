def fidelity_firewall(amount, trust_score, velocity, variance):
    """Rejects structurally malformed or impossible transaction payloads."""
    if amount <= 0 or amount > 50000:
        return False, "Invalid transaction boundary limit"
    if not (0.0 <= trust_score <= 1.0):
        return False, "Malformed biometric/device trust signature"
    if velocity < 1 or velocity > 100:
        return False, "Velocity out of realistic human scale"
    return True, "Passed Structural Integrity Firewall"

def evaluate_enterprise_decision(probability):
    """Maps risk scores to the 4-tier decision framework from the architecture diagram."""
    if probability < 0.30:
        return "ALLOW", "🟢 Low Risk: Seamless frictionless checkout allowed."
    elif probability < 0.60:
        return "STEP-UP", "🟡 Moderate Risk: Trigger multi-factor authentication / biometric challenge."
    elif probability < 0.85:
        return "REVIEW", "🟠 High Risk: Route profile to human Fraud Analyst Queue."
    else:
        return "BLOCK", "🔴 Critical Threat Vector: Immediate automated transaction decline."