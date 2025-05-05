import sys
from config.settings import BASE_DIR
sys.path.append(f"{BASE_DIR}/insurance")
from django.contrib import admin
from .models import DynamicSchema, DynamicCategory, DynamicField
from django import forms
from insurance.models import (
    InsuredUser,
    InsuranceCompany,
    InsurancePolicy,
    PolicyType,
    EmployerCompany,
)
from django.db import models

MODEL_REGISTRY = {
    "InsuredUser": InsuredUser,
    "InsuranceCompany": InsuranceCompany,
    "EmployerCompany": EmployerCompany,
    "PolicyType": PolicyType,
    "InsurancePolicy": InsurancePolicy,
}


class DynamicFieldAdminForm(forms.ModelForm):
    class Meta:
        model = DynamicField
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        instance = kwargs.get("instance")
        category = instance.category if instance else self.initial.get("category")

        if category and category.name in MODEL_REGISTRY:
            model_class = MODEL_REGISTRY[category.name]

            field_names = [
                f.name
                for f in model_class._meta.get_fields()
                if isinstance(f, models.Field) and not f.auto_created
            ]
            self.fields["mapped_name"].widget = forms.Select(
                choices=[(f, f) for f in field_names]
            )
        else:
            self.fields["mapped_name"].widget = forms.TextInput()


class DynamicFieldInline(admin.TabularInline):
    model = DynamicField
    extra = 1
    fields = ("name", "mapped_name", "data_type", "required", "default_value")
    show_change_link = True


class DynamicCategoryInline(admin.TabularInline):
    model = DynamicCategory
    extra = 1
    fields = ("name",)
    show_change_link = True


@admin.register(DynamicSchema)
class DynamicSchemaAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "created_at")
    inlines = [DynamicCategoryInline]


@admin.register(DynamicCategory)
class DynamicCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "schema")
    inlines = [DynamicFieldInline]
    list_filter = ("name",)
    search_fields = ("name",)



@admin.register(DynamicField)
class DynamicFieldAdmin(admin.ModelAdmin):
    form = DynamicFieldAdminForm
    list_display = (
        "name",
        "mapped_name",
        "data_type",
        "required",
        "default_value",
        "category",
    )
    list_filter = ("data_type", "required", "category")
    search_fields = ("name", "mapped_name")
