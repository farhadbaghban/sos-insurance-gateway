from typing import Any, Dict, List, Type

from rest_framework import serializers
from rest_framework.exceptions import ValidationError


FIELD_TYPE_MAP = {
    "string": serializers.CharField,
    "integer": serializers.IntegerField,
    "boolean": serializers.BooleanField,
    "datetime": serializers.DateTimeField,
    "date": serializers.DateField,
    "float": serializers.FloatField,
}


def declare_serializer_fields(
    field_list: List[Dict[str, Any]], category: str
) -> Type[serializers.Serializer]:
    fields = {}
    for field in field_list:
        data_type = field.get("data_type")
        field_type_class = FIELD_TYPE_MAP.get(data_type)
        if not field_type_class:
            raise ValidationError(
                f"Unsupported data type: '{data_type}' in category '{category}'"
            )
        field_kwargs = {
            "required": field.get("required", False),
            "source": field.get("name"),
        }

        default = field.get("default_value")
        if default is not None:
            field_kwargs["default"] = default

        fields[field["mapped_name"]] = field_type_class(**field_kwargs)

    return type(f"{category.capitalize()}Serializer", (serializers.Serializer,), fields)


def generate_serializer_class(
    field_map: Dict[str, List[Dict[str, Any]]],
) -> Type[serializers.Serializer]:
    nested_serializers = {}

    for category, field_list in field_map.items():
        if not isinstance(field_list, list):
            raise ValidationError(
                f"Field list for '{category}' must be a list of fields."
            )

        nested_serializer_class = declare_serializer_fields(field_list, category)
        nested_serializers[category] = nested_serializer_class()

    return type("DynamicInputSerializer", (serializers.Serializer,), nested_serializers)
