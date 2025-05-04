from django.db import models


class DynamicSchema(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class DynamicField(models.Model):
    DATA_TYPE_CHOICES = [
        ("string", "String"),
        ("integer", "Integer"),
        ("boolean", "Boolean"),
        ("date", "Date"),
        ("datetime", "DateTime"),
        ("float", "Float"),
    ]

    schema = models.ForeignKey(
        DynamicSchema, on_delete=models.CASCADE, related_name="fields"
    )
    name = models.CharField(max_length=100)
    mapped_name = models.CharField(max_length=100)
    data_type = models.CharField(choices=DATA_TYPE_CHOICES, max_length=20)
    required = models.BooleanField(default=False)
    default_value = models.CharField(max_length=255, null=True, blank=True)
