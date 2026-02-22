import csv
from pathlib import Path

from conversion_rate_mlops.domain.schema import validate_required_columns


class CsvDatasetAdapter:
    def load_training(self, csv_path: Path) -> tuple[list[dict], list[int]]:
        rows: list[dict] = []
        labels: list[int] = []
        with csv_path.open("r", encoding="utf-8", newline="") as file_handle:
            reader = csv.DictReader(file_handle)
            missing = validate_required_columns(reader.fieldnames or [])
            if missing:
                raise ValueError(f"Missing required columns: {', '.join(missing)}")

            for row in reader:
                labels.append(int(row.pop("converted")))
                rows.append(row)
        return rows, labels

    def load_inference(self, csv_path: Path) -> list[dict]:
        with csv_path.open("r", encoding="utf-8", newline="") as file_handle:
            reader = csv.DictReader(file_handle)
            required = ["country", "age", "new_user", "source", "total_pages_visited"]
            missing = [name for name in required if name not in (reader.fieldnames or [])]
            if missing:
                raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")
            return list(reader)
