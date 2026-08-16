import os
import sys
import pytest
from pydantic import ValidationError

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.golden_validator import validate_golden_dataset

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../agents')))
from schemas.evaluation_schemas import ChatbotGoldenDataset

GOLDEN_FILE = os.path.join(os.path.dirname(__file__), '../test_data/ai/chatbot_goldens.json')

def test_chatbot_golden_dataset_parses_successfully():
    """Verify that the master golden dataset is valid and has at least 30 items."""
    dataset = validate_golden_dataset(GOLDEN_FILE)
    
    assert dataset is not None
    assert len(dataset.goldens) == 37
    
    # Ensure all categories are represented (just a spot check)
    categories = set([g.category.value for g in dataset.goldens])
    assert "allergy" in categories
    assert "prompt injection" in categories
    assert "conflicting constraints" in categories

def test_chatbot_golden_dataset_rejects_duplicates():
    """Verify that the schema validator correctly rejects duplicate golden_ids."""
    duplicate_data = {
        "goldens": [
            {
                "golden_id": "DUP-01",
                "category": "basic",
                "conversation": [{"role": "user", "content": "hi"}],
                "expected_behavior": "test"
            },
            {
                "golden_id": "DUP-01", # Duplicate ID!
                "category": "basic",
                "conversation": [{"role": "user", "content": "hello"}],
                "expected_behavior": "test2"
            }
        ]
    }
    
    with pytest.raises(ValidationError) as exc_info:
        ChatbotGoldenDataset.model_validate(duplicate_data)
    
    assert "Duplicate golden_ids found: DUP-01" in str(exc_info.value)
