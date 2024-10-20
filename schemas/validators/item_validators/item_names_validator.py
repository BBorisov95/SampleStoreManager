from schemas.validators.empty_string_checker import is_empty_string


def validate_item_name(item_name: str):

    is_empty_string(item_name, "Item Name")
