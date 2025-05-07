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


def create_dynamic_serializer_class(class_name):
    dynamic_class = type(f"{class_name}Serializer", (serializers.Serializer,), {})

    return dynamic_class


def declare_serializer_fields(
    field_list: List[Dict[str, Any]], category: str
) -> Type[serializers.Serializer]:
    read_only_fields = {"id", "created_at", "updated_at", "is_deleted"}
    serializer_class = create_dynamic_serializer_class(category)
    for field in field_list:
        name = field.get("name")
        mapped_name = field.get("mapped_name")
        required = field.get("required", False)
        default = field.get("default_value")
        data_type = field.get("data_type")

        field_type_class = FIELD_TYPE_MAP.get(data_type)
        if not field_type_class:
            raise serializers.ValidationError(
                f"Unsupported data type: '{data_type}' in category '{category}'"
            )

        field_kwargs = {}
        if mapped_name in read_only_fields:
            field_kwargs["read_only"] = True
        else:
            field_kwargs["required"] = required
            if not required and default is not None:
                field_kwargs["default"] = default

        if name != mapped_name:
            field_kwargs["source"] = name
        serializer_class._declared_fields[mapped_name] = field_type_class(
            **field_kwargs
        )
    return serializer_class


def generate_serializer_class(
    field_map: Dict[str, List[Dict[str, Any]]],
) -> Type[serializers.Serializer]:
    class DynamicInputSerializer(serializers.Serializer):
        pass

    for category, field_list in field_map.items():
        if not isinstance(field_list, list):
            raise ValidationError(
                f"Field list for '{category}' must be a list of fields."
            )

        nested_serializer_class = declare_serializer_fields(field_list, category)
        DynamicInputSerializer._declared_fields[category] = nested_serializer_class()
    return DynamicInputSerializer
