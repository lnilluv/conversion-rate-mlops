import unittest
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))

from conversion_rate_mlops.domain.schema import REQUIRED_COLUMNS, validate_required_columns


class DomainSchemaTests(unittest.TestCase):
    def test_validate_required_columns_accepts_complete_schema(self) -> None:
        missing = validate_required_columns(list(REQUIRED_COLUMNS))
        self.assertEqual(missing, [])

    def test_validate_required_columns_returns_missing_columns(self) -> None:
        missing = validate_required_columns(["country", "age", "source"])
        self.assertEqual(missing, ["converted", "new_user", "total_pages_visited"])


if __name__ == "__main__":
    unittest.main()
