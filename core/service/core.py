import json
from pathlib import Path


def load_json(*, path):
    project_dir = Path(__file__).resolve().parents[2]
    json_path = project_dir / path
    with json_path.open("r", encoding="utf-8") as file:
        return json.load(file)