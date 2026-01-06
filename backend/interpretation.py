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
    "TSH": (0.3, 4.2)
}


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


def extract_abnormal_findings(parsed_values: dict):
    abnormalities = []

    for test, value in parsed_values.items():
        status = classify_value(test, value)
        if status and status != "NORMAL":
            abnormalities.append(
                f"{test}: {status} ({value})"
            )

    return abnormalities
