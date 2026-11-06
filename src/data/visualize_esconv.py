
"""
Generate visualizations for ESConv dataset analysis.
"""

import json
from pathlib import Path
from collections import Counter
import matplotlib.pyplot as plt

# Locate project and processed dataset
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_DIR = PROJECT_ROOT / "docs" / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

files = [
    DATA_DIR / "esconv_train.jsonl",
    DATA_DIR / "esconv_validation.jsonl",
    DATA_DIR / "esconv_test.jsonl"
]

conversations = []

for file_path in files:
    if not file_path.exists():
        raise FileNotFoundError(f"Dataset file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                conversations.append(json.loads(line))

print("Total conversations loaded:", len(conversations))

# Collect dataset information
emotions = Counter()
problems = Counter()
strategies = Counter()

for conversation in conversations:
    emotion = conversation.get("emotion_type")
    problem = conversation.get("problem_type")

    if emotion:
        emotions[str(emotion).strip()] += 1

    if problem:
        problems[str(problem).strip()] += 1

    for turn in conversation.get("dialog", []):
        strategy = turn.get("strategy")

        if strategy:
            strategies[str(strategy).strip()] += 1


def create_chart(counter, title, filename, color=None):
    labels, values = zip(*counter.most_common())

    plt.figure(figsize=(12, 6))
    plt.bar(labels, values, color=color)
    plt.title(title, fontsize=15)
    plt.xlabel("Category")
    plt.ylabel("Count")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    output_path = OUTPUT_DIR / filename
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()

    print("Saved:", output_path)


# 1. Emotion distribution
create_chart(
    emotions,
    "ESConv Emotion Distribution",
    "emotion_distribution.png"
)

# 2. Problem type distribution
create_chart(
    problems,
    "ESConv Problem Type Distribution",
    "problem_distribution.png"
)

# 3. Supporter strategy distribution
create_chart(
    strategies,
    "ESConv Supporter Strategy Distribution",
    "strategy_distribution.png"
)

print("\nAll three visualizations generated successfully!")
