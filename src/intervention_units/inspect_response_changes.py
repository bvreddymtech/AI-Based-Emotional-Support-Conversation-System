"""
Inspect and sample Intervention Unit records from processed ESConv splits.

This script loads the initial Intervention Unit JSONL files, draws a reproducible
random sample of intervention units from each split (train, validation, test),
and displays the contextual dialogue sequence:
    previous_user_text -> supporter_text (with strategy) -> next_user_text
along with conversation-level metadata to inspect how users respond to
different emotional support interventions.
"""

import json
import random
from pathlib import Path


def load_jsonl(file_path):
    """
    Safely load records from a JSONL file.

    Args:
        file_path (Path or str): Path to the JSONL file.

    Returns:
        list[dict]: Parsed list of JSON records.
    """
    path = Path(file_path)
    if not path.exists():
        print(f"Warning: File not found at {path}")
        return []

    records = []
    with open(path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            line_str = line.strip()
            if not line_str:
                continue
            try:
                records.append(json.loads(line_str))
            except (json.JSONDecodeError, TypeError) as e:
                print(f"Warning: Failed to parse line {line_num} in {path.name}: {e}")
    return records


def display_sample(unit, sample_idx, total_samples):
    """
    Print a single intervention unit in a clean, readable format.

    Args:
        unit (dict): The intervention unit record dictionary.
        sample_idx (int): Current sample number (1-indexed).
        total_samples (int): Total number of samples in this split.
    """
    split = unit.get("split", "unknown").upper()
    conv_id = unit.get("conversation_id", "N/A")
    turn_idx = unit.get("turn_index", "N/A")
    emotion = unit.get("emotion_type", "N/A")
    problem = unit.get("problem_type", "N/A")
    strategy = unit.get("support_strategy", "N/A")

    prev_user = unit.get("previous_user_text", "")
    supporter = unit.get("supporter_text", "")
    next_user = unit.get("next_user_text", "")

    print(f"\n  {'─' * 66}")
    print(f"  [Sample {sample_idx}/{total_samples}] {conv_id} (Turn {turn_idx}) | Split: {split}")
    print(f"  {'─' * 66}")
    print(f"  • Emotion Type:     {emotion}")
    print(f"  • Problem Type:     {problem}")
    print(f"  • Support Strategy: {strategy}")
    print("\n  [1] Previous User (Seeker) Text:")
    print(f"      \"{prev_user}\"")
    print(f"\n  [2] Supporter Intervention ({strategy}):")
    print(f"      \"{supporter}\"")
    print("\n  [3] Next User (Seeker) Response:")
    print(f"      \"{next_user}\"")


def inspect_split(records, split_name, num_samples=3, seed=42):
    """
    Sample and display intervention units for a specific split.

    Args:
        records (list[dict]): List of records for the split.
        split_name (str): Name of the split ('train', 'validation', 'test').
        num_samples (int): Number of samples to draw.
        seed (int): Random seed for reproducibility.

    Returns:
        int: Number of samples actually inspected.
    """
    separator = "=" * 70
    print("\n" + separator)
    print(f" INSPECTING SPLIT: {split_name.upper()}")
    print(separator)

    if not records:
        print(f"  No records found for split '{split_name}'.")
        return 0

    # Deterministic sampling per split
    rng = random.Random(seed)
    sample_size = min(num_samples, len(records))
    samples = rng.sample(records, sample_size)

    for idx, unit in enumerate(samples, start=1):
        display_sample(unit, idx, sample_size)

    return sample_size


def main():
    """
    Main inspection pipeline:
    1. Loads train, validation, and test intervention unit files.
    2. Draws reproducible random samples from each split.
    3. Prints detailed sequence context for qualitative review.
    4. Displays an overall inspection summary.
    """
    data_dir = Path("data/processed")

    split_files = {
        "train": data_dir / "intervention_units_train.jsonl",
        "validation": data_dir / "intervention_units_validation.jsonl",
        "test": data_dir / "intervention_units_test.jsonl",
    }

    # Configuration: fixed seed for reproducibility, 3 samples per split
    random_seed = 42
    samples_per_split = 3

    inspection_counts = {}
    total_records_map = {}

    print("\n======================================================================")
    print(" INTERVENTION UNIT RESPONSE INSPECTION")
    print(f" (Seed: {random_seed}, Samples per split: {samples_per_split})")
    print("======================================================================")

    for split_name, file_path in split_files.items():
        records = load_jsonl(file_path)
        total_records_map[split_name] = len(records)
        inspected_count = inspect_split(
            records=records,
            split_name=split_name,
            num_samples=samples_per_split,
            seed=random_seed,
        )
        inspection_counts[split_name] = inspected_count

    # Summary Section
    summary_sep = "=" * 70
    print("\n" + summary_sep)
    print(" INSPECTION SUMMARY")
    print(summary_sep)
    total_inspected = sum(inspection_counts.values())
    for split_name, count in inspection_counts.items():
        total = total_records_map.get(split_name, 0)
        print(f"  • {split_name.capitalize()} Split:    {count} samples inspected (from {total:,} total units)")
    print(f"  • Total Inspected: {total_inspected} samples across all splits")
    print(summary_sep + "\n")


if __name__ == "__main__":
    main()
