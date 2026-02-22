import csv
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))

from conversion_rate_mlops.adapters.csv_dataset import CsvDatasetAdapter
from conversion_rate_mlops.adapters.rule_based_model import RuleBasedClassificationAdapter


class AdapterTests(unittest.TestCase):
    def test_csv_dataset_adapter_reads_training_rows(self) -> None:
        adapter = CsvDatasetAdapter()
        with tempfile.TemporaryDirectory() as tmp_dir:
            csv_path = Path(tmp_dir) / "train.csv"
            with csv_path.open("w", encoding="utf-8", newline="") as file_handle:
                writer = csv.writer(file_handle)
                writer.writerow(
                    [
                        "country",
                        "age",
                        "new_user",
                        "source",
                        "total_pages_visited",
                        "converted",
                    ]
                )
                writer.writerow(["US", "30", "0", "Seo", "7", "1"])

            rows, labels = adapter.load_training(csv_path)

        self.assertEqual(labels, [1])
        self.assertEqual(rows[0]["country"], "US")

    def test_rule_based_adapter_predicts_from_threshold(self) -> None:
        adapter = RuleBasedClassificationAdapter()
        model = adapter.train(
            rows=[
                {"total_pages_visited": "2"},
                {"total_pages_visited": "12"},
            ],
            labels=[0, 1],
        )

        predictions = adapter.predict(
            model=model,
            rows=[
                {"total_pages_visited": "1"},
                {"total_pages_visited": "20"},
            ],
        )

        self.assertEqual(predictions, [0, 1])


if __name__ == "__main__":
    unittest.main()
