# Conversion Rate MLOps Repository

This repository showcases the productionized version of the original Conversion Rate challenge, refactored from notebook-first experimentation into a deployable ML service-style project.

## What was improved

- Split the initial multi-project repository into three dedicated repos to improve ownership and deployment scope:
  - `https://github.com/lnilluv/conversion-rate-mlops`
  - `https://github.com/lnilluv/uber-hotzone-ml`
  - `https://github.com/lnilluv/walmart-sales-forecast`
- Introduced hexagonal architecture in production paths (`domain`, `application`, `adapters`, `bootstrap`)
- Added CLI entrypoints for deterministic local/VPS execution
- Added smoke tests and Docker workflows for reproducible runtime checks
- Hardened repository security posture (`.env` strategy, artifact ignore rules, dependency audits)

## Active project in this repo

- `conversion_rate/`

## Quick start

```bash
cd conversion_rate
export PYTHONPATH=src
python3 -m unittest discover -s tests/unit -p 'test_*.py'
./scripts/smoke_test.sh
```
