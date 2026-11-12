import json
from pathlib import Path

PATH_TO_FILE = Path(__file__).resolve().parent.parent / "data" / "category_routing.json"

class CategoryRoutingUseCase:
    def __init__(self) -> None:
        # open json file and load it into a dict
        with open(PATH_TO_FILE, encoding="utf-8") as f:
            departments = json.load(f)

        # build reverse dict
        category_to_dept = {}
        for department, categories in departments.items():
            for category in categories:
                category_to_dept[category] = department

        self._category_to_dept = category_to_dept

    def execute(self, category: str) -> str:
        """Method that takes a category and returns the department it belongs to"""
        if category in self._category_to_dept:
            return self._category_to_dept[category]
        raise ValueError(f"Category '{category}' not found in data.")
