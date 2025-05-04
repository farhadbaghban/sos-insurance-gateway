from typing import Dict, List, Any
from ...schema.models import DynamicCategory


def get_dynamic_schema_for_serializer(schema_name: str):
    categories = DynamicCategory.objects.filter(
        schema__name=schema_name
    ).prefetch_related("fields")

    category_list = []
    result: Dict[str, List[Dict[str, Any]]] = {}

    for category in categories:
        category_list.append(category)
        result[category.name] = [
            {
                "name": field.name,
                "mapped_name": field.mapped_name,
                "data_type": field.data_type,
                "required": field.required,
                "default_value": field.default_value,
            }
            for field in category.fields.all()
        ]

    return result, category_list
