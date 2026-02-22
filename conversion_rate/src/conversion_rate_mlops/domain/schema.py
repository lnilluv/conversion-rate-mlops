REQUIRED_COLUMNS = [
    "country",
    "age",
    "new_user",
    "source",
    "total_pages_visited",
    "converted",
]


def validate_required_columns(column_names: list[str]) -> list[str]:
    columns = set(column_names)
    return sorted([name for name in REQUIRED_COLUMNS if name not in columns])
