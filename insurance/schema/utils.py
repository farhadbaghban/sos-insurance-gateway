from typing import Dict, List, Any
from rest_framework.exceptions import ValidationError

DATA_TYPE_MAPPING = {
    "string": str,
    "integer": int,
    "boolean": bool,
    "float": float,
    "date": str,
    "datetime": str,
}


def map_and_validate_input(field_map: Dict[str, List[Dict[str, Any]]], input_data):
    errors = []

    for category_name, fields in field_map.items():
        category_data = input_data.get(category_name, {})
        category_errors = {}

        for field in fields:
            field_name = field["name"]
            required = field["required"]
            default = field["default_value"]
            data_type = field["data_type"]
            python_type = DATA_TYPE_MAPPING.get(data_type)

            value = category_data.get(field_name)

            if value is None or value == "":
                if required:
                    if default:
                        value = default
                    else:
                        category_errors[field_name] = "This field is required."
                        continue
            if not isinstance(value, python_type):
                category_errors[field_name] = (
                    f"Invalid type for field '{field_name}'. Expected {data_type}."
                )
                continue
        if category_errors:
            errors.append({category_name: category_errors})

    if errors:
        raise ValidationError(errors)
    else:
        return True
