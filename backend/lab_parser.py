# lab_parser.py
import re

TEST_NAMES = [
    "Haemoglobin",
    "Total WBC Count",
    "Neutrophil",
    "Lymphocytes",
    "Eosinophil",
    "Monocytes",
    "Basophils",
    "MCV",
    "MCH",
    "MCHC",
    "Platelet Count",
    "ESR",
    "TSH"
]


def parse_lab_values(text: str) -> dict:
    results = {}

    lines = text.splitlines()

    for line in lines:
        for test in TEST_NAMES:
            if test.lower() in line.lower():
                numbers = re.findall(r"\d+\.?\d*", line)
                if numbers:
                    try:
                        results[test] = float(numbers[0])
                    except:
                        pass

    return results
