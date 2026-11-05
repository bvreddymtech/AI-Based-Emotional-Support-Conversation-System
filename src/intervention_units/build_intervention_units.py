"""
Build an initial Intervention Unit representation from processed ESConv dataset.

This script processes dialogue turns from the train, validation, and test splits
of ESConv. For each supporter turn with an annotated support strategy, it extracts
the contextual triad:
    (previous_user_text, supporter_text [with strategy], next_user_text)
along with conversation-level metadata (emotion_type, problem_type, situation, etc.).

Note:
This represents an initial ESConv-based intervention structure. It preserves
conversation-level metadata and dataset strategy labels without inventing turn-level
emotional states or mapping to higher-level skill taxonomies.
"""

import json
from collections import Counter
from pathlib import Path


def is_seeker_turn(turn):
    """
    Check if a dialogue turn belongs to the seeker/user.

    Args:
        turn (dict): Dialogue turn dictionary.

    Returns:
        bool: True if speaker represents the user/seeker.
    """
    speaker = str(turn.get("speaker", "")).lower().strip()
    return speaker in ("usr", "user", "seeker")


def is_supporter_turn(turn):
    """
    Check if a dialogue turn belongs to the supporter/system.

    Args:
        turn (dict): Dialogue turn dictionary.

    Returns:
        bool: True if speaker represents the supporter/system.
    """
    speaker = str(turn.get("speaker", "")).lower().strip()
    return speaker in ("sys", "system", "supporter")


def find_surrounding_seeker_turns(dialog, supporter_idx):
    """
    Find the closest preceding and following seeker turns for a supporter turn.

    Args:
        dialog (list[dict]): Full list of dialogue turns.
        supporter_idx (int): Index of the current supporter turn.

    Returns:
        tuple[dict | None, dict | None]: (previous_seeker_turn, next_seeker_turn)
    """
    prev_turn = None
    next_turn = None

    # Search backward for the closest preceding seeker turn
    for i in range(supporter_idx - 1, -1, -1):
        if is_seeker_turn(dialog[i]):
            prev_turn = dialog[i]
            break

    # Search forward for the closest following seeker turn
    for i in range(supporter_idx + 1, len(dialog)):
        if is_seeker_turn(dialog[i]):
            next_turn = dialog[i]
            break

    return prev_turn, next_turn


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


def save_jsonl(records, output_path):
    """
    Save a list of dictionaries to a JSONL file.

    Args:
        records (list[dict]): List of dictionaries to save.
        output_path (Path or str): Destination file path.
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


def extract_intervention_units(conversations, split_name):
    """
    Extract intervention unit records from a list of conversations.

    Args:
        conversations (list[dict]): List of conversation dictionaries.
        split_name (str): The name of the split ('train', 'validation', 'test').

    Returns:
        tuple[list[dict], int, Counter]:
            - extracted_units: List of structured intervention unit records.
            - skipped_count: Number of supporter turns skipped due to missing surrounding seeker turns.
            - strategy_counts: Frequency distribution of extracted support strategies.
    """
    extracted_units = []
    skipped_count = 0
    strategy_counts = Counter()

    for conv in conversations:
        conversation_id = conv.get("conversation_id")
        experience_type = conv.get("experience_type")
        emotion_type = conv.get("emotion_type")
        problem_type = conv.get("problem_type")
        situation = conv.get("situation")

        dialog = conv.get("dialog", [])
        if not isinstance(dialog, list):
            continue

        for turn_idx, turn in enumerate(dialog):
            if not isinstance(turn, dict):
                continue

            strategy = turn.get("strategy")
            # Only process supporter/system turns that have an annotated strategy
            if not strategy or not is_supporter_turn(turn):
                continue

            supporter_text = str(turn.get("text", "")).strip()

            # Find closest preceding and following seeker turns
            prev_user_turn, next_user_turn = find_surrounding_seeker_turns(dialog, turn_idx)

            # If either surrounding seeker turn does not exist, skip this supporter turn
            if prev_user_turn is None or next_user_turn is None:
                skipped_count += 1
                continue

            prev_user_text = str(prev_user_turn.get("text", "")).strip()
            next_user_text = str(next_user_turn.get("text", "")).strip()
            strategy_str = str(strategy).strip()

            strategy_counts[strategy_str] += 1

            record = {
                "conversation_id": conversation_id,
                "turn_index": turn_idx,
                "experience_type": experience_type,
                "emotion_type": emotion_type,
                "problem_type": problem_type,
                "situation": situation,
                "previous_user_text": prev_user_text,
                "supporter_text": supporter_text,
                "support_strategy": strategy_str,
                "next_user_text": next_user_text,
                "split": split_name,
            }

            extracted_units.append(record)

    return extracted_units, skipped_count, strategy_counts


def print_split_summary(split_name, num_records, skipped_count, strategy_counts, output_file):
    """
    Print a summary of the extraction process for a single split.

    Args:
        split_name (str): Name of the split.
        num_records (int): Total records successfully extracted.
        skipped_count (int): Number of skipped turns.
        strategy_counts (Counter): Support strategy distribution.
        output_file (Path): Saved output file path.
    """
    print(f"\n{'=' * 60}")
    print(f" Split: {split_name.upper()}")
    print(f"{'=' * 60}")
    print(f"  - Intervention Units Created: {num_records}")
    print(f"  - Supporter Turns Skipped (no surrounding seeker): {skipped_count}")
    print(f"  - Output File: {output_file}")
    print("  - Strategy Distribution:")
    for strat, count in sorted(strategy_counts.items(), key=lambda x: -x[1]):
        print(f"      * {strat}: {count}")


def main():
    """
    Main extraction pipeline:
    1. Reads processed train, validation, and test ESConv JSONL files.
    2. Extracts intervention units matching the (previous_user, supporter, next_user) pattern.
    3. Saves structured records to data/processed/intervention_units_<split>.jsonl.
    4. Prints extraction statistics for each split and overall totals.
    """
    data_dir = Path("data/processed")

    splits = {
        "train": {
            "input": data_dir / "esconv_train.jsonl",
            "output": data_dir / "intervention_units_train.jsonl",
        },
        "validation": {
            "input": data_dir / "esconv_validation.jsonl",
            "output": data_dir / "intervention_units_validation.jsonl",
        },
        "test": {
            "input": data_dir / "esconv_test.jsonl",
            "output": data_dir / "intervention_units_test.jsonl",
        },
    }

    total_records = 0
    total_skipped = 0
    overall_strategy_counts = Counter()

    print("\n--- Building Initial Intervention Units from ESConv ---")

    for split_name, paths in splits.items():
        input_file = paths["input"]
        output_file = paths["output"]

        conversations = load_jsonl(input_file)
        if not conversations:
            print(f"Skipping split '{split_name}' (no records in {input_file}).")
            continue

        units, skipped, strat_counts = extract_intervention_units(conversations, split_name)

        # Save to processed directory
        save_jsonl(units, output_file)

        # Print per-split summary
        print_split_summary(split_name, len(units), skipped, strat_counts, output_file)

        # Accumulate totals
        total_records += len(units)
        total_skipped += skipped
        overall_strategy_counts.update(strat_counts)

    # Print overall summary across all splits
    print(f"\n{'=' * 60}")
    print(" TOTAL ACROSS ALL SPLITS")
    print(f"{'=' * 60}")
    print(f"  - Total Intervention Units Created: {total_records}")
    print(f"  - Total Supporter Turns Skipped:    {total_skipped}")
    print("  - Overall Strategy Distribution:")
    for strat, count in sorted(overall_strategy_counts.items(), key=lambda x: -x[1]):
        print(f"      * {strat}: {count}")
    print("\nIntervention unit extraction complete!\n")


if __name__ == "__main__":
    main()
