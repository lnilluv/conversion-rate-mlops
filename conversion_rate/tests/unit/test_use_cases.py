import unittest
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))

from conversion_rate_mlops.application.ports import DatasetPort, ModelPort, ModelRegistryPort
from conversion_rate_mlops.application.use_cases import predict_from_csv, train_from_csv


class FakeDatasetAdapter(DatasetPort):
    def load_training(self, csv_path: Path) -> tuple[list[dict], list[int]]:
        return ([{"country": "US"}], [1])

    def load_inference(self, csv_path: Path) -> list[dict]:
        return [{"country": "US"}]


class FakeModelAdapter(ModelPort):
    def train(self, rows: list[dict], labels: list[int]) -> object:
        return {"trained": True, "labels": labels}

    def predict(self, model: object, rows: list[dict]) -> list[int]:
        return [1 for _ in rows]


class FakeRegistryAdapter(ModelRegistryPort):
    def __init__(self) -> None:
        self.saved = False
        self.loaded = False

    def save(self, model: object, path: Path) -> None:
        self.saved = True

    def load(self, path: Path) -> object:
        self.loaded = True
        return {"trained": True}


class UseCaseTests(unittest.TestCase):
    def test_train_from_csv_trains_and_saves_model(self) -> None:
        dataset = FakeDatasetAdapter()
        model = FakeModelAdapter()
        registry = FakeRegistryAdapter()
        tmp_path = Path(".")

        train_from_csv(
            dataset_port=dataset,
            model_port=model,
            registry_port=registry,
            train_csv_path=tmp_path / "train.csv",
            model_output_path=tmp_path / "model.joblib",
        )

        self.assertTrue(registry.saved)

    def test_predict_from_csv_loads_model_and_returns_predictions(self) -> None:
        dataset = FakeDatasetAdapter()
        model = FakeModelAdapter()
        registry = FakeRegistryAdapter()
        tmp_path = Path(".")

        predictions = predict_from_csv(
            dataset_port=dataset,
            model_port=model,
            registry_port=registry,
            inference_csv_path=tmp_path / "test.csv",
            model_path=tmp_path / "model.joblib",
        )

        self.assertTrue(registry.loaded)
        self.assertEqual(predictions, [1])


if __name__ == "__main__":
    unittest.main()
