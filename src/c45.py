"""Small categorical C4.5-style decision tree using gain ratio."""
from collections import Counter
from math import log2

def entropy(labels):
    counts = Counter(labels)
    total = len(labels)
    return -sum((n / total) * log2(n / total) for n in counts.values() if n)

def gain_ratio(rows, attribute, target):
    base = entropy([row[target] for row in rows])
    groups = {}
    for row in rows:
        groups.setdefault(row[attribute], []).append(row)
    remainder = sum(len(group) / len(rows) * entropy([r[target] for r in group])
                    for group in groups.values())
    gain = base - remainder
    split_info = entropy([row[attribute] for row in rows])
    return (gain / split_info if split_info else 0.0), groups

def fit(rows, attributes, target="hanh_dong"):
    labels = [row[target] for row in rows]
    counts = Counter(labels)
    if len(counts) == 1:
        return {"leaf": labels[0], "counts": dict(counts)}
    if not attributes:
        return {"leaf": counts.most_common(1)[0][0], "counts": dict(counts)}
    scored = [(gain_ratio(rows, attr, target)[0], attr) for attr in attributes]
    score, best = max(scored)
    if score <= 0:
        return {"leaf": counts.most_common(1)[0][0], "counts": dict(counts)}
    _, groups = gain_ratio(rows, best, target)
    remaining = [attr for attr in attributes if attr != best]
    return {"attribute": best, "gain_ratio": score, "counts": dict(counts),
            "branches": {value: fit(group, remaining, target)
                         for value, group in sorted(groups.items())},
            "fallback": counts.most_common(1)[0][0]}

def predict(tree, sample):
    if "leaf" in tree:
        return tree["leaf"]
    branch = tree["branches"].get(sample.get(tree["attribute"]))
    return predict(branch, sample) if branch else tree["fallback"]

def print_tree(tree, indent=""):
    if "leaf" in tree:
        print(f"{indent}→ {tree['leaf']}")
        return
    print(f"{indent}[{tree['attribute']}] (Gain Ratio={tree['gain_ratio']:.3f})")
    for value, child in tree["branches"].items():
        print(f"{indent}  {value}:")
        print_tree(child, indent + "    ")
