# interpretation.py

NORMAL_RANGES = {
    "Haemoglobin": (12, 16),
    "Total WBC Count": (4000, 11000),
    "Neutrophil": (40, 70),
    "Lymphocytes": (20, 40),
    "Eosinophil": (1, 4),
    "Monocytes": (2, 8),
    "Basophils": (0, 1),
    "MCV": (80, 100),
    "MCH": (27, 32),
    "MCHC": (32, 36),
    "Platelet Count": (150000, 450000),
    "ESR": (0, 20),

    "TSH": (0.3, 4.2),
    "THYROID STIMULATING HORMONE": (0.3, 4.2),
    "T3": (1.23, 3.07),
    "T4": (66, 181),

    "Glucose Fasting": (60, 110),
    "Glucose PP": (90, 160)
}


# ======================================================
# 🔥 NEW: SEVERITY CALCULATION
# ======================================================
def calculate_severity(test_name, value):
    if test_name not in NORMAL_RANGES:
        return "Unknown"

    low, high = NORMAL_RANGES[test_name]

    if value < low * 0.7:
        return "Severely Low"
    elif value < low:
        return "Mildly Low"
    elif value > high * 1.3:
        return "Severely High"
    elif value > high:
        return "Mildly High"
    else:
        return "Normal"


# ======================================================
# 🔥 UPGRADED CONDITION DETECTION
# ======================================================
def detect_conditions(abnormal_findings):
    conditions = []

    findings_text = " ".join(abnormal_findings)

    # Anemia
    if "Haemoglobin" in findings_text:
        if "LOW" in findings_text:
            conditions.append("Anemia (low hemoglobin)")

    if "MCV: LOW" in findings_text:
        conditions.append("Microcytic anemia (possible iron deficiency)")

    # Inflammation
    if "ESR: HIGH" in findings_text:
        conditions.append("Inflammatory condition or infection")

    # Diabetes
    if "Glucose Fasting: HIGH" in findings_text or "Glucose PP: HIGH" in findings_text:
        conditions.append("Risk of diabetes or impaired glucose metabolism")

    # Thyroid
    if "TSH: HIGH" in findings_text:
        conditions.append("Hypothyroidism")

    if "TSH: LOW" in findings_text:
        conditions.append("Hyperthyroidism")

    return list(set(conditions))  # remove duplicates


# ======================================================
# EXISTING
# ======================================================
def classify_value(test_name, value):
    if test_name not in NORMAL_RANGES:
        return None

    low, high = NORMAL_RANGES[test_name]

    if value < low:
        return "LOW"
    elif value > high:
        return "HIGH"
    else:
        return "NORMAL"


# ======================================================
# 🔥 UPDATED ABNORMAL FINDINGS (WITH SEVERITY)
# ======================================================
def extract_abnormal_findings(parsed_values: dict):
    abnormalities = []

    for test, value in parsed_values.items():
        status = classify_value(test, value)

        if status and status != "NORMAL":
            severity = calculate_severity(test, value)

            abnormalities.append(
                f"{test}: {status} ({value}) [{severity}]"
            )

    return abnormalities
