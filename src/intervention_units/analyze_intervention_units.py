"""
Analyze initial Intervention Unit dataset files.

This script inspects the processed Intervention Unit JSONL files across
train, validation, and test splits. It computes distributions of:
- Total records and unique conversations
- emotion_type, problem_type, experience_type, and support_strategy
- support_strategy co-occurrences with emotion_type and problem_type
and prints detailed reports per split as well as an overall aggregate summary.
"""

import json
from collections import Counter, defaultdict
from pathlib import Path


def load_jsonl(file_path):
    """
    Safely load records from a JSONL file.

    Args:
        file_path (Path or str): Path to the JSONL file.

    Returns:
        list[dict]: Parsed list of JSON objects.
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


def analyze_records(records, split_name="Split"):
    """
    Compute statistical distributions and co-occurrences for intervention records.

    Args:
        records (list[dict]): List of intervention unit records.
        split_name (str): Label for the current dataset split.

    Returns:
        dict: Aggregated distribution metrics.
    """
    total_records = len(records)
    unique_conversations = len({
        r.get("conversation_id") for r in records if r.get("conversation_id")
    })

    emotion_counts = Counter()
    problem_counts = Counter()
    experience_counts = Counter()
    strategy_counts = Counter()

    strategy_emotion_map = defaultdict(Counter)
    strategy_problem_map = defaultdict(Counter)

    for r in records:
        emotion = str(r.get("emotion_type") or "(Missing)").strip()
        problem = str(r.get("problem_type") or "(Missing)").strip()
        experience = str(r.get("experience_type") or "(Missing)").strip()
        strategy = str(r.get("support_strategy") or "(Missing)").strip()

        emotion_counts[emotion] += 1
        problem_counts[problem] += 1
        experience_counts[experience] += 1
        strategy_counts[strategy] += 1

        strategy_emotion_map[strategy][emotion] += 1
        strategy_problem_map[strategy][problem] += 1

    return {
        "split_name": split_name,
        "total_records": total_records,
        "unique_conversations": unique_conversations,
        "emotion_counts": emotion_counts,
        "problem_counts": problem_counts,
        "experience_counts": experience_counts,
        "strategy_counts": strategy_counts,
        "strategy_emotion_map": strategy_emotion_map,
        "strategy_problem_map": strategy_problem_map,
    }


def print_counter(counter, title, indent=2):
    """
    Print counts from a Counter sorted descending by frequency.

    Args:
        counter (Counter): Counter dictionary.
        title (str): Section header.
        indent (int): Number of leading spaces.
    """
    prefix = " " * indent
    print(f"\n{prefix}--- {title} ---")
    if not counter:
        print(f"{prefix}  (None recorded)")
        return

    for key, count in sorted(counter.items(), key=lambda item: (-item[1], str(item[0]))):
        print(f"{prefix}  - {key}: {count}")


def print_nested_breakdown(nested_map, title, primary_label="Strategy", secondary_label="Category", indent=2):
    """
    Print a nested two-level breakdown (e.g., strategy -> emotion_type).

    Args:
        nested_map (dict[str, Counter]): Outer key -> Counter of inner keys.
        title (str): Section title.
        primary_label (str): Label for outer key.
        secondary_label (str): Label for inner key.
        indent (int): Indentation level.
    """
    prefix = " " * indent
    print(f"\n{prefix}--- {title} ---")
    if not nested_map:
        print(f"{prefix}  (None recorded)")
        return

    # Sort primary keys by total count across their secondary items
    sorted_primaries = sorted(
        nested_map.items(),
        key=lambda item: -sum(item[1].values())
    )

    for primary, sec_counter in sorted_primaries:
        total_for_primary = sum(sec_counter.values())
        print(f"{prefix}  * {primary} (Total: {total_for_primary})")
        for secondary, count in sorted(sec_counter.items(), key=lambda item: (-item[1], str(item[0]))):
            print(f"{prefix}      - {secondary}: {count}")


def print_analysis_report(stats):
    """
    Print formatted terminal report for an analysis result dictionary.

    Args:
        stats (dict): Dictionary output from analyze_records().
    """
    separator = "=" * 70
    print("\n" + separator)
    print(f" INTERVENTION UNITS ANALYSIS: {stats['split_name'].upper()}")
    print(separator)
    print(f"  Total Intervention Records:        {stats['total_records']}")
    print(f"  Unique Conversations Represented:  {stats['unique_conversations']}")

    # 1D Distributions
    print_counter(stats["emotion_counts"], "Distribution of emotion_type")
    print_counter(stats["problem_counts"], "Distribution of problem_type")
    print_counter(stats["experience_counts"], "Distribution of experience_type")
    print_counter(stats["strategy_counts"], "Distribution of support_strategy")

    # 2D Co-occurrences
    print_nested_breakdown(
        stats["strategy_emotion_map"],
        "Records by support_strategy + emotion_type",
        primary_label="Strategy",
        secondary_label="Emotion",
    )
    print_nested_breakdown(
        stats["strategy_problem_map"],
        "Records by support_strategy + problem_type",
        primary_label="Strategy",
        secondary_label="Problem",
    )


def main():
    """
    Main analysis pipeline:
    1. Loads intervention unit JSONL files for train, validation, and test splits.
    2. Runs distribution and co-occurrence analysis for each split.
    3. Aggregates records across all splits and prints an overall summary.
    """
    data_dir = Path("data/processed")

    split_files = {
        "Train": data_dir / "intervention_units_train.jsonl",
        "Validation": data_dir / "intervention_units_validation.jsonl",
        "Test": data_dir / "intervention_units_test.jsonl",
    }

    all_records = []

    print("\nStarting Intervention Units Analysis...")

    # Analyze each split individually
    for split_name, file_path in split_files.items():
        records = load_jsonl(file_path)
        if not records:
            print(f"\nSkipping split '{split_name}' (no data found at {file_path}).")
            continue

        all_records.extend(records)
        stats = analyze_records(records, split_name=split_name)
        print_analysis_report(stats)

    # Analyze aggregate total across all splits
    if all_records:
        total_stats = analyze_records(all_records, split_name="Total Across All Splits")
        print_analysis_report(total_stats)
    else:
        print("\nNo intervention unit records found. Please run build_intervention_units.py first.")

    print("\nIntervention units analysis complete!\n")


if __name__ == "__main__":
    main()
