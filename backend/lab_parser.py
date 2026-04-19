# lab_parser.py
import re

# 🔥 Canonical test names + aliases
TEST_ALIASES = {
    "Haemoglobin": ["Haemoglobin", "Hemoglobin", "Hb"],
    "Total WBC Count": ["Total WBC Count", "WBC", "WBC Count"],
    "Neutrophil": ["Neutrophil"],
    "Lymphocytes": ["Lymphocytes"],
    "Eosinophil": ["Eosinophil"],
    "Monocytes": ["Monocytes"],
    "Basophils": ["Basophils"],
    "MCV": ["MCV"],
    "MCH": ["MCH"],
    "MCHC": ["MCHC"],
    "Platelet Count": ["Platelet Count", "Platelets"],
    "ESR": ["ESR"],
    "TSH": ["TSH", "THYROID STIMULATING HORMONE"],
    "T3": ["T3", "TRIIODOTHYRONINE"],
    "T4": ["T4", "THYROXINE"],
    "Glucose Fasting": ["Glucose Fasting", "Fasting Glucose"],
    "Glucose PP": ["Glucose PP", "Postprandial Glucose"]
}


def extract_number_from_line(line):
    """
    Extract the most likely lab value (NOT reference range)
    """
    numbers = re.findall(r"\d+\.?\d*", line)

    if not numbers:
        return None

    # 🔥 heuristic:
    # usually first number after test name is correct
    return float(numbers[0])


def parse_lab_values(text: str) -> dict:
    results = {}
    lines = text.splitlines()

    for line in lines:
        line_lower = line.lower()

        for canonical, aliases in TEST_ALIASES.items():
            for alias in aliases:
                if alias.lower() in line_lower:

                    value = extract_number_from_line(line)

                    if value is not None:
                        # 🔥 don't overwrite if already found better value
                        if canonical not in results:
                            results[canonical] = value

                    break  # stop checking more aliases

    return results
