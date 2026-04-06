# SLANG-Money — Reference Demonstration
# Deterministic structural resolution

import hashlib
import json

# -------------------------------
# RULES (structure definition)
# -------------------------------

rules = [
    ("A_final", "50", lambda s: s.get("A_initial") == "100" and s.get("delta_A") == "-50"),
    ("B_final", "150", lambda s: s.get("B_initial") == "100" and s.get("delta_B") == "50"),
    ("state", "resolved", lambda s: s.get("A_final") == "50" and s.get("B_final") == "150"),
]

# -------------------------------
# INITIAL STATE
# -------------------------------

state = {
    "A_initial": "100",
    "B_initial": "100",
    "delta_A": "-50",
    "delta_B": "50"
}

# -------------------------------
# RESOLUTION ENGINE
# -------------------------------

TRACE = False  # set True for step-by-step visibility

changed = True

while changed:
    changed = False
    for key, value, cond in rules:
        if cond(state) and state.get(key) != value:
            state[key] = value
            changed = True
            if TRACE:
                print(f"-> Set {key} = {value} | state: {state}")

# -------------------------------
# STRUCTURAL MATURITY
# -------------------------------

def is_structure_mature(s):
    return s.get("state") == "resolved"

# -------------------------------
# ORDERED STRUCTURE (VISIBLE STATE)
# -------------------------------

order = ["A_initial", "B_initial", "delta_A", "delta_B", "A_final", "B_final", "state"]

visible_state = {k: state[k] for k in order if k in state}

# -------------------------------
# STRUCTURAL CERTIFICATE
# -------------------------------

def structural_certificate(s):
    normalized = json.dumps(s, sort_keys=True)
    return hashlib.sha256(normalized.encode()).hexdigest()

# -------------------------------
# OUTPUT
# -------------------------------

print("\nVISIBLE STATE:")
print(visible_state)

print("\nSTRUCTURAL MATURITY:")
print(is_structure_mature(state))

print("\nSTRUCTURAL CERTIFICATE:")
print(structural_certificate(visible_state))