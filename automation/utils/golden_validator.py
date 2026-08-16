import json
import sys
import os
from pydantic import ValidationError

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../agents')))
from agents.infrastructure.schemas.evaluation_schemas import ChatbotGoldenDataset, AgentGoldenDataset

def validate_golden_dataset(filepath: str) -> ChatbotGoldenDataset:
    """
    Loads and validates a JSON file containing chatbot goldens against the 
    ChatbotGoldenDataset Pydantic schema.
    Returns the parsed dataset if valid. Raises ValidationError or ValueError otherwise.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Golden dataset not found at {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Validate using Pydantic
    try:
        dataset = ChatbotGoldenDataset.model_validate(data)
        return dataset
    except ValidationError as e:
        print(f"Schema Validation Failed for {filepath}")
        print(e)
        raise

def validate_agent_golden_dataset(filepath: str) -> AgentGoldenDataset:
    """
    Loads and validates a JSON file containing agent goldens against the 
    AgentGoldenDataset Pydantic schema.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Agent golden dataset not found at {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    try:
        dataset = AgentGoldenDataset.model_validate(data)
        return dataset
    except ValidationError as e:
        print(f"Schema Validation Failed for {filepath}")
        print(e)
        raise

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Validate a Chatbot Golden Dataset")
    parser.add_argument("filepath", type=str, help="Path to the JSON file")
    args = parser.parse_args()

    try:
        dataset = validate_golden_dataset(args.filepath)
        print(f"Success! Validated {len(dataset.goldens)} goldens.")
    except Exception as e:
        sys.exit(1)
