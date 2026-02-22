from pathlib import Path

from conversion_rate_mlops.application.ports import DatasetPort, ModelPort, ModelRegistryPort


def train_from_csv(
    dataset_port: DatasetPort,
    model_port: ModelPort,
    registry_port: ModelRegistryPort,
    train_csv_path: Path,
    model_output_path: Path,
) -> None:
    rows, labels = dataset_port.load_training(train_csv_path)
    model = model_port.train(rows, labels)
    registry_port.save(model, model_output_path)


def predict_from_csv(
    dataset_port: DatasetPort,
    model_port: ModelPort,
    registry_port: ModelRegistryPort,
    inference_csv_path: Path,
    model_path: Path,
) -> list[int]:
    rows = dataset_port.load_inference(inference_csv_path)
    model = registry_port.load(model_path)
    return model_port.predict(model, rows)
