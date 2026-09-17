"""
Preprocess the ESConv (thu-coai/esconv) dataset from Hugging Face
into clean JSONL files for our research project.
"""

import json
from pathlib import Path
from datasets import load_dataset


def load_esconv():
    """
    Load the ESConv dataset from Hugging Face Hub.

    Returns:
        DatasetDict: The loaded dataset containing train, validation, and test splits.
    """
    print("Loading 'thu-coai/esconv' dataset from Hugging Face...")
    return load_dataset("thu-coai/esconv")


def process_split(dataset_split, split_name):
    """
    Process a single dataset split by parsing JSON strings and extracting fields.

    Args:
        dataset_split: The Hugging Face dataset split (e.g., train, validation, test).
        split_name (str): Name of the split ('train', 'validation', 'test').

    Returns:
        list[dict]: List of cleaned and structured conversation dictionaries.
    """
    processed_conversations = []
    conv_index = 1

    for idx, example in enumerate(dataset_split):
        raw_text = example.get("text")
        if not raw_text:
            print(f"Warning: Missing 'text' field at index {idx} in {split_name} split. Skipping.")
            continue

        # Basic error handling for malformed JSON records
        try:
            parsed = json.loads(raw_text)
        except (json.JSONDecodeError, TypeError) as e:
            print(f"Warning: Failed to parse JSON at index {idx} in {split_name} split: {e}. Skipping.")
            continue

        # Generate unique conversation ID (e.g., train_0001, validation_0001)
        conversation_id = f"{split_name}_{conv_index:04d}"
        conv_index += 1

        # Extract dialog turns cleanly
        raw_dialog = parsed.get("dialog", [])
        clean_dialog = []
        for turn in raw_dialog:
            turn_data = {
                "speaker": turn.get("speaker"),
                "text": turn.get("text", turn.get("content", "")),
            }
            # Preserve strategy when present
            if "strategy" in turn and turn["strategy"] is not None:
                turn_data["strategy"] = turn["strategy"]
            clean_dialog.append(turn_data)

        # Preserve conversation-level fields
        conversation_record = {
            "conversation_id": conversation_id,
            "experience_type": parsed.get("experience_type"),
            "emotion_type": parsed.get("emotion_type"),
            "problem_type": parsed.get("problem_type"),
            "situation": parsed.get("situation"),
            "survey_score": parsed.get("survey_score"),
            "seeker_question1": parsed.get("seeker_question1"),
            "seeker_question2": parsed.get("seeker_question2"),
            "supporter_question1": parsed.get("supporter_question1"),
            "supporter_question2": parsed.get("supporter_question2"),
            "dialog": clean_dialog,
        }

        processed_conversations.append(conversation_record)

    return processed_conversations


def save_jsonl(records, output_path):
    """
    Save a list of conversation records to a JSONL file.

    Args:
        records (list[dict]): List of conversation dictionaries.
        output_path (Path): Destination file path.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


def main():
    """
    Main preprocessing pipeline:
    1. Loads ESConv dataset from Hugging Face.
    2. Processes train, validation, and test splits.
    3. Saves clean JSONL files into data/processed/.
    4. Prints summary information for each split.
    """
    # Define output directory and ensure it exists
    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Load the dataset
    dataset = load_esconv()

    # 2. Define splits to process
    splits = ["train", "validation", "test"]

    print("\n--- Processing ESConv Dataset ---")
    for split_name in splits:
        if split_name not in dataset:
            print(f"Warning: Split '{split_name}' not found in dataset. Skipping.")
            continue

        # Process the split
        processed_records = process_split(dataset[split_name], split_name)

        # Define output path
        output_file = output_dir / f"esconv_{split_name}.jsonl"

        # Save to JSONL
        save_jsonl(processed_records, output_file)

        # Print summary
        print(f"Split: {split_name} | Conversations: {len(processed_records)} | Output: {output_file}")

    print("\nPreprocessing complete!")


if __name__ == "__main__":
    main()
