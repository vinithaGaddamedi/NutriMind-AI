import csv
import json
import os
from typing import List, Dict, Any

class DataLoader:
    """
    Utility loader for test data from CSV, JSON, or mock generators.
    """

    @staticmethod
    def load_csv(file_path: str) -> List[Dict[str, str]]:
        """
        Loads CSV file rows into a list of dictionaries.
        """
        resolved_path = os.path.abspath(file_path)
        if not os.path.exists(resolved_path):
            raise FileNotFoundError(f"Test data CSV file not found at: {resolved_path}")

        results = []
        with open(resolved_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                results.append(dict(row))
        return results

    @staticmethod
    def load_json(file_path: str) -> Dict[str, Any]:
        """
        Loads JSON file into a dictionary or list.
        """
        resolved_path = os.path.abspath(file_path)
        if not os.path.exists(resolved_path):
            raise FileNotFoundError(f"Test data JSON file not found at: {resolved_path}")

        with open(resolved_path, mode="r", encoding="utf-8") as f:
            return json.load(f)
