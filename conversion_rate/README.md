# Conversion Rate MLOps

Production-ready rewrite of the conversion-rate challenge: from exploratory notebooks to a modular, testable, and VPS-friendly ML workflow.

## Portfolio highlights

- Refactored into hexagonal architecture to separate business logic from infrastructure concerns
- Added command-line application flow for `train` and `predict`
- Added unit tests for domain, adapters, and application use cases
- Added end-to-end smoke test script to validate real execution
- Added Docker image for reproducible deployment
- Added dependency vulnerability scanning with `pip-audit`

## Project layout

- `src/conversion_rate_mlops/domain/`: business rules and schema validation
- `src/conversion_rate_mlops/application/`: use cases and ports
- `src/conversion_rate_mlops/adapters/`: CSV IO, rule-based model adapter, model registry
- `src/conversion_rate_mlops/bootstrap/`: CLI composition root
- `tests/unit/`: unit tests for domain and application layers
- `scripts/smoke_test.sh`: end-to-end train/predict smoke test

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
export PYTHONPATH=src
python -m unittest discover -s tests/unit -p 'test_*.py'
./scripts/smoke_test.sh
```

## CLI usage

Train model:

```bash
python3 -m conversion_rate_mlops.bootstrap.cli train \
  --train-csv conversion_data_train.csv \
  --model-output artifacts/model.joblib
```

Predict:

```bash
python3 -m conversion_rate_mlops.bootstrap.cli predict \
  --inference-csv conversion_data_test.csv \
  --model-path artifacts/model.joblib \
  --output-csv artifacts/predictions.csv
```

## Docker

```bash
docker build -t conversion-rate-mlops:local .
docker run --rm -v "$PWD/artifacts:/app/artifacts" conversion-rate-mlops:local \
  train --train-csv /app/conversion_data_train.csv --model-output /app/artifacts/model.joblib

docker run --rm -v "$PWD/artifacts:/app/artifacts" conversion-rate-mlops:local \
  predict --inference-csv /app/conversion_data_test.csv --model-path /app/artifacts/model.joblib --output-csv /app/artifacts/predictions.csv
```

## Security notes

- `.env` files are ignored; use `.env.example` as template.
- Generated artifacts under `artifacts/` are ignored.
- Run `pip-audit -r requirements.txt` before release.
