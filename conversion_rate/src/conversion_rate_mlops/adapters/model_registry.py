from pathlib import Path
import pickle

class PickleModelRegistryAdapter:
    def save(self, model: object, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("wb") as file_handle:
            pickle.dump(model, file_handle)

    def load(self, path: Path) -> object:
        with path.open("rb") as file_handle:
            return pickle.load(file_handle)
