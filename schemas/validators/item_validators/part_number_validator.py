from schemas.validators.item_validators.empty_string_checker import is_empty_string


def validate_part_number(part_number: str):
    is_empty_string(part_number, "Part number")
