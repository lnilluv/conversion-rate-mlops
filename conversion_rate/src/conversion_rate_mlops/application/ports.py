from pathlib import Path
from typing import Protocol


class DatasetPort(Protocol):
    def load_training(self, csv_path: Path) -> tuple[list[dict], list[int]]: ...

    def load_inference(self, csv_path: Path) -> list[dict]: ...


class ModelPort(Protocol):
    def train(self, rows: list[dict], labels: list[int]) -> object: ...

    def predict(self, model: object, rows: list[dict]) -> list[int]: ...


class ModelRegistryPort(Protocol):
    def save(self, model: object, path: Path) -> None: ...

    def load(self, path: Path) -> object: ...
