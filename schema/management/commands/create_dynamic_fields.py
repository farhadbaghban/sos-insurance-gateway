from django.core.management.base import BaseCommand
from django.db import models
from django.contrib.auth.models import User
from schema.models import (
    DynamicSchema,
    DynamicCategory,
    DynamicField,
)
from insurance.models import (
    InsuredUser,
    InsuranceCompany,
    EmployerCompany,
    PolicyType,
    InsurancePolicy,
)


class Command(BaseCommand):
    help = "Creates dynamic field configurations for models"

    def handle(self, *args, **kwargs):
        read_only_fields = {"id", "created_at", "updated_at", "is_deleted"}

        MODEL_MAP = {
            "InsuredUser": InsuredUser,
            "InsuranceCompany": InsuranceCompany,
            "EmployerCompany": EmployerCompany,
            "PolicyType": PolicyType,
            "InsurancePolicy": InsurancePolicy,
        }

        FIELD_TYPE_MAPPING = {
            models.CharField: "string",
            models.TextField: "string",
            models.EmailField: "string",
            models.IntegerField: "integer",
            models.BooleanField: "boolean",
            models.DateField: "date",
            models.DateTimeField: "datetime",
            models.FloatField: "float",
            models.DecimalField: "float",
            models.ForeignKey: "integer",
        }

        def get_data_type(field):
            for field_class, data_type in FIELD_TYPE_MAPPING.items():
                if isinstance(field, field_class):
                    return data_type
            return "string"

        user = User.objects.first()
        schema, _ = DynamicSchema.objects.get_or_create(name="saman", user=user)

        for model_name, model in MODEL_MAP.items():
            category, _ = DynamicCategory.objects.get_or_create(
                name=model_name, schema=schema
            )

            for field in model._meta.get_fields():
                if isinstance(field, models.Field):
                    if field.name in read_only_fields:
                        continue
                    data_type = get_data_type(field)
                    DynamicField.objects.get_or_create(
                        category=category,
                        name=field.name,
                        mapped_name=field.name,
                        data_type=data_type,
                        required=not field.null,
                        default_value=field.default
                        if field.default not in (models.NOT_PROVIDED, None)
                        else "",
                    )

        self.stdout.write(self.style.SUCCESS("Dynamic fields created successfully."))
