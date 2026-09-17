"""
Analyze processed ESConv JSONL dataset files.

This script inspects the train, validation, and test splits of ESConv,
calculates key dataset statistics (distributions of emotions, problems,
experiences, supporter strategies, and turn statistics), and prints
both per-split and overall summary reports to the terminal.
"""

import json
from collections import Counter
from pathlib import Path


def load_jsonl(file_path):
    """
    Safely load records from a JSONL file.

    Args:
        file_path (Path or str): Path to the JSONL file.

    Returns:
        list[dict]: List of parsed JSON objects.
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
                data = json.loads(line_str)
                records.append(data)
            except (json.JSONDecodeError, TypeError) as e:
                print(f"Warning: Could not parse JSON on line {line_num} in {path.name}: {e}")
    return records


def analyze_split(conversations, split_name="Split"):
    """
    Calculate statistics for a list of conversation records.

    Args:
        conversations (list[dict]): List of conversation dictionaries.
        split_name (str): Label for the current dataset split.

    Returns:
        dict: Aggregated statistical metrics.
    """
    num_conversations = len(conversations)

    emotion_counts = Counter()
    problem_counts = Counter()
    experience_counts = Counter()
    strategy_counts = Counter()

    dialog_lengths = []
    total_seeker_turns = 0
    total_supporter_turns = 0

    for conv in conversations:
        # 1. Emotion type
        emotion = conv.get("emotion_type")
        emotion_counts[str(emotion).strip() if emotion else "(Missing)"] += 1

        # 2. Problem type
        problem = conv.get("problem_type")
        problem_counts[str(problem).strip() if problem else "(Missing)"] += 1

        # 3. Experience type
        experience = conv.get("experience_type")
        experience_counts[str(experience).strip() if experience else "(Missing)"] += 1

        # 4. Dialogue turns
        dialog = conv.get("dialog", [])
        if not isinstance(dialog, list):
            dialog = []

        dialog_lengths.append(len(dialog))

        for turn in dialog:
            if not isinstance(turn, dict):
                continue

            speaker = str(turn.get("speaker", "")).lower().strip()
            strategy = turn.get("strategy")

            # Identify speaker category
            if speaker in ("usr", "user", "seeker"):
                total_seeker_turns += 1
            elif speaker in ("sys", "system", "supporter"):
                total_supporter_turns += 1

            # Count supporter strategy if present
            if strategy:
                strategy_counts[str(strategy).strip()] += 1

    # Compute turn summary statistics
    min_turns = min(dialog_lengths) if dialog_lengths else 0
    max_turns = max(dialog_lengths) if dialog_lengths else 0
    avg_turns = sum(dialog_lengths) / len(dialog_lengths) if dialog_lengths else 0.0
    total_turns = sum(dialog_lengths)

    return {
        "split_name": split_name,
        "num_conversations": num_conversations,
        "emotion_counts": emotion_counts,
        "problem_counts": problem_counts,
        "experience_counts": experience_counts,
        "strategy_counts": strategy_counts,
        "min_turns": min_turns,
        "max_turns": max_turns,
        "avg_turns": avg_turns,
        "total_seeker_turns": total_seeker_turns,
        "total_supporter_turns": total_supporter_turns,
        "total_turns": total_turns,
    }


def print_counter(counter, title, indent=2):
    """
    Print formatted key-value counts from a Counter.

    Args:
        counter (Counter): Counter object containing frequency counts.
        title (str): Header title for the section.
        indent (int): Number of spaces to indent.
    """
    prefix = " " * indent
    print(f"\n{prefix}--- {title} ---")
    if not counter:
        print(f"{prefix}  (None recorded)")
        return

    # Sort by frequency descending, then alphabetically by name
    for key, count in sorted(counter.items(), key=lambda item: (-item[1], str(item[0]))):
        print(f"{prefix}  - {key}: {count}")


def print_split_analysis(stats):
    """
    Print a comprehensive formatted report for a single analysis dictionary.

    Args:
        stats (dict): Dictionary output from analyze_split().
    """
    separator = "=" * 65
    print("\n" + separator)
    print(f" DATASET ANALYSIS: {stats['split_name'].upper()}")
    print(separator)
    print(f"  Total Conversations: {stats['num_conversations']}")

    # Print distributions
    print_counter(stats["emotion_counts"], "Emotion Types (emotion_type)")
    print_counter(stats["problem_counts"], "Problem Types (problem_type)")
    print_counter(stats["experience_counts"], "Experience Types (experience_type)")
    print_counter(stats["strategy_counts"], "Supporter Strategies (strategy)")

    # Print dialogue turn statistics
    print("\n  --- Dialogue Turn Statistics ---")
    print(f"    - Min turns per conversation: {stats['min_turns']}")
    print(f"    - Max turns per conversation: {stats['max_turns']}")
    print(f"    - Avg turns per conversation: {stats['avg_turns']:.2f}")
    print(f"    - Total Seeker (User) turns:   {stats['total_seeker_turns']}")
    print(f"    - Total Supporter (Sys) turns: {stats['total_supporter_turns']}")
    print(f"    - Total Dialogue turns:        {stats['total_turns']}")


def main():
    """
    Main analysis workflow:
    1. Locates and loads train, validation, and test processed JSONL files.
    2. Runs analysis on each split individually and prints results.
    3. Runs aggregated analysis across all splits and prints total statistics.
    """
    data_dir = Path("data/processed")

    split_files = {
        "Train": data_dir / "esconv_train.jsonl",
        "Validation": data_dir / "esconv_validation.jsonl",
        "Test": data_dir / "esconv_test.jsonl",
    }

    all_conversations = []

    print("\nStarting ESConv Dataset Analysis...")

    # Analyze each split separately
    for split_name, file_path in split_files.items():
        records = load_jsonl(file_path)
        if not records:
            print(f"\nSkipping split '{split_name}' (no data found at {file_path}).")
            continue

        all_conversations.extend(records)
        stats = analyze_split(records, split_name=split_name)
        print_split_analysis(stats)

    # Analyze combined total across all splits
    if all_conversations:
        total_stats = analyze_split(all_conversations, split_name="Total Across All Splits")
        print_split_analysis(total_stats)
    else:
        print("\nNo conversations found across any splits. Please run preprocess_esconv.py first.")

    print("\nAnalysis complete!\n")


if __name__ == "__main__":
    main()
