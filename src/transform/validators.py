from typing import List
from src.transform.models import CleanedRecord


def validate_record(record: CleanedRecord) -> tuple[bool, str | None]:
    if record.year < 2000 or record.year > 2030:
        return False, f"Invalid year: {record.year}"
    if record.category == "gdp" and (record.value < -50 or record.value > 50):
        return False, f"GDP value out of range: {record.value}"
    if record.category == "inflation" and (record.value < -20 or record.value > 100):
        return False, f"Inflation value out of range: {record.value}"
    if not record.country_name:
        return False, "Missing country name"
    return True, None


def validate_batch(records: List[CleanedRecord]) -> dict:
    total = len(records)
    invalid = [r for r in records if not validate_record(r)[0]]
    return {
        "total": total,
        "valid": total - len(invalid),
        "invalid": len(invalid),
        "invalid_records": [
            {"indicator": r.indicator_name, "error": validate_record(r)[1]}
            for r in invalid
        ],
    }