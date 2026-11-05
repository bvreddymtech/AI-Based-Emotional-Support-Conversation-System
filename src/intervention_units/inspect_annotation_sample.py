"""
Generate a human-readable inspection and manual annotation report
from the 100-sample Intervention Unit dataset.

This script reads `data/processed/annotation_sample_100.jsonl` and generates
a structured text document (`data/processed/annotation_sample_100_inspection.txt`).
Each section contains all original conversational context fields along with an
empty annotation template for manual research labeling.
"""

import json
from pathlib import Path


def load_jsonl(file_path):
    """
    Safely load JSONL records from a given file path.

    Args:
        file_path (Path or str): Path to the input JSONL file.

    Returns:
        list[dict]: List of parsed JSON record dictionaries.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found at: {path}")

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


def format_sample_section(record, sample_num, total_samples):
    """
    Format a single Intervention Unit record into a structured text section
    with original fields and an empty annotation template.

    Args:
        record (dict): Intervention unit dictionary.
        sample_num (int): 1-indexed sample sequence number.
        total_samples (int): Total number of samples.

    Returns:
        str: Formatted text section for the record.
    """
    conv_id = record.get("conversation_id", "N/A")
    turn_idx = record.get("turn_index", "N/A")
    split = record.get("split", "N/A")
    status = record.get("annotation_status", "pending")

    exp_type = record.get("experience_type", "N/A")
    emo_type = record.get("emotion_type", "N/A")
    prob_type = record.get("problem_type", "N/A")
    situation = record.get("situation", "N/A")

    prev_user = record.get("previous_user_text", "")
    supporter = record.get("supporter_text", "")
    strategy = record.get("support_strategy", "N/A")
    next_user = record.get("next_user_text", "")

    separator = "=" * 80
    sub_sep = "-" * 80

    lines = [
        separator,
        f" SAMPLE {sample_num:03d} / {total_samples:03d}",
        separator,
        f"Conversation ID:    {conv_id}",
        f"Turn Index:         {turn_idx}",
        f"Split:              {split}",
        f"Annotation Status:  {status}",
        "",
        "Context Metadata:",
        f"  • Experience Type: {exp_type}",
        f"  • Emotion Type:    {emo_type}",
        f"  • Problem Type:    {prob_type}",
        f"  • Situation:       {situation}",
        "",
        "Dialogue Sequence:",
        "  [Previous User / Seeker Text]:",
        f"    {prev_user}",
        "",
        f"  [Supporter Intervention (Strategy: {strategy})]:",
        f"    {supporter}",
        "",
        "  [Next User / Seeker Response]:",
        f"    {next_user}",
        "",
        sub_sep,
        " Manual Annotation Template:",
        sub_sep,
        "Pre-Seeker State:",
        "Fine-Grained Support Action:",
        "Response Change:",
        "Change Direction:",
        "Post-Seeker State:",
        "Annotation Notes:",
        "",
        "\n",
    ]

    return "\n".join(lines)


def generate_inspection_report(records, output_path):
    """
    Generate and save the full inspection report for all records.

    Args:
        records (list[dict]): List of 100 intervention unit records.
        output_path (Path or str): Output file path.

    Returns:
        int: Total number of records written to the report.
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    total_samples = len(records)
    header = [
        "#" * 80,
        "# INTERVENTION UNIT MANUAL ANNOTATION & INSPECTION REPORT",
        f"# Total Records: {total_samples}",
        "# Source: data/processed/annotation_sample_100.jsonl",
        "#" * 80,
        "\n\n",
    ]

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(header))
        for idx, rec in enumerate(records, start=1):
            section_text = format_sample_section(rec, idx, total_samples)
            f.write(section_text)

    return total_samples


def main():
    """
    Main execution pipeline:
    1. Loads data/processed/annotation_sample_100.jsonl.
    2. Verifies that exactly 100 records are present.
    3. Formats each record with context, dialogue, and manual annotation template.
    4. Writes report to data/processed/annotation_sample_100_inspection.txt.
    5. Prints summary.
    """
    input_path = Path("data/processed/annotation_sample_100.jsonl")
    output_path = Path("data/processed/annotation_sample_100_inspection.txt")

    print("\n--- Generating Human-Readable Annotation Inspection Report ---")

    # 1. Load input records
    records = load_jsonl(input_path)
    record_count = len(records)

    # 2. Verify record count
    if record_count != 100:
        raise ValueError(
            f"Expected exactly 100 records in {input_path}, but found {record_count}."
        )

    # 3. Generate report
    written_count = generate_inspection_report(records, output_path)

    # 4. Verify output written count
    if written_count != 100:
        raise RuntimeError(
            f"Verification error: Expected to write 100 sections, wrote {written_count}."
        )

    # 5. Print summary
    print(f"  • Input File:         {input_path}")
    print(f"  • Records Inspected:  {written_count}")
    print(f"  • Output Report:      {output_path}")
    print("\nInspection report generated successfully!\n")


if __name__ == "__main__":
    main()
