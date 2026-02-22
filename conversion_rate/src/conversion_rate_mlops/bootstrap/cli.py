import argparse
import csv
from pathlib import Path

from conversion_rate_mlops.adapters.csv_dataset import CsvDatasetAdapter
from conversion_rate_mlops.adapters.model_registry import PickleModelRegistryAdapter
from conversion_rate_mlops.adapters.rule_based_model import RuleBasedClassificationAdapter
from conversion_rate_mlops.application.use_cases import predict_from_csv, train_from_csv


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Conversion Rate MLOps CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    train_parser = subparsers.add_parser("train", help="Train and persist a model")
    train_parser.add_argument("--train-csv", required=True)
    train_parser.add_argument("--model-output", required=True)

    predict_parser = subparsers.add_parser("predict", help="Generate predictions")
    predict_parser.add_argument("--inference-csv", required=True)
    predict_parser.add_argument("--model-path", required=True)
    predict_parser.add_argument("--output-csv", required=True)

    return parser


def main() -> None:
    args = _build_parser().parse_args()
    dataset_adapter = CsvDatasetAdapter()
    model_adapter = RuleBasedClassificationAdapter()
    registry_adapter = PickleModelRegistryAdapter()

    if args.command == "train":
        train_from_csv(
            dataset_port=dataset_adapter,
            model_port=model_adapter,
            registry_port=registry_adapter,
            train_csv_path=Path(args.train_csv),
            model_output_path=Path(args.model_output),
        )
        print(f"Model saved to {args.model_output}")
        return

    predictions = predict_from_csv(
        dataset_port=dataset_adapter,
        model_port=model_adapter,
        registry_port=registry_adapter,
        inference_csv_path=Path(args.inference_csv),
        model_path=Path(args.model_path),
    )
    output_path = Path(args.output_csv)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as file_handle:
        writer = csv.writer(file_handle)
        writer.writerow(["prediction"])
        for value in predictions:
            writer.writerow([value])
    print(f"Predictions saved to {args.output_csv}")


if __name__ == "__main__":
    main()
