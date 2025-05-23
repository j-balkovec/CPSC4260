# This script opens the report (MI returned by radon scan)
#   and classifies it, since radon doesn't provide that for JSON outputs

import json

RADON_MI_FILE = "radon_mi.json"

def rank_mi(mi):
    thresholds = {
        "A": 85,
        "B": 70,
        "C": 60,
        "D": 40,
        "F": 0,
    }
    for rank in ["A", "B", "C", "D", "F"]:
        if mi >= thresholds[rank]:
            return rank

with open(RADON_MI_FILE, "r") as radon_file:
    mi_dict = json.load(radon_file)

for filename, metrics in mi_dict.items():
    metrics['rank'] = rank_mi(metrics['mi'])

with open(RADON_MI_FILE, "w") as radon_file:
    json.dump(mi_dict, radon_file, indent=4)

