from django.db import models
from django.contrib.auth.models import User


class DynamicSchema(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)


class DynamicCategory(models.Model):
    CATEGORY_MODEL_CHOICES = [
        ("InsuredUser", "InsuredUser"),
        ("InsuranceCompany", "InsuranceCompany"),
        ("EmployerCompany", "EmployerCompany"),
        ("PolicyType", "PolicyType"),
        ("InsurancePolicy", "InsurancePolicy"),
    ]
    name = models.CharField(max_length=100, choices=CATEGORY_MODEL_CHOICES)
    schema = models.ForeignKey(
        DynamicSchema, on_delete=models.CASCADE, related_name="category"
    )

    def __str__(self):
        return self.name


class DynamicField(models.Model):
    DATA_TYPE_CHOICES = [
        ("string", "String"),
        ("integer", "Integer"),
        ("boolean", "Boolean"),
        ("date", "Date"),
        ("datetime", "DateTime"),
        ("float", "Float"),
    ]
    category = models.ForeignKey(
        DynamicCategory, on_delete=models.CASCADE, related_name="fields"
    )

    name = models.CharField(max_length=100)
    mapped_name = models.CharField(
        max_length=100, help_text="The actual model field name (e.g. id_card_number)"
    )
    data_type = models.CharField(choices=DATA_TYPE_CHOICES, max_length=20)
    required = models.BooleanField(default=False)
    default_value = models.CharField(max_length=255, null=True, blank=True)
