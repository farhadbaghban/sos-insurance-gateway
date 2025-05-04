from django.db import models
from .validators import (
    validate_iranian_phone,
    validate_and_normalize_id_card,
    normalize_iranian_phone,
)


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()


class InsuredUser(BaseModel):
    name = models.CharField(max_length=100, null=True, blank=True)
    family_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    id_card_number = models.CharField(max_length=50, unique=True)
    birthday = models.DateField(null=True, blank=True)
    father_name = models.CharField(max_length=100, null=True, blank=True)
    birthday_city = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(
        max_length=13, validators=[validate_iranian_phone], unique=True
    )

    def clean(self):
        super().clean()
        self.id_card_number = validate_and_normalize_id_card(self.id_card_number)
        self.phone_number = normalize_iranian_phone(self.phone_number)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class InsuranceCompany(BaseModel):
    name = models.CharField(max_length=100, null=True, blank=True)
    unique_code = models.CharField(max_length=50, unique=True)


class EmployerCompany(BaseModel):
    name = models.CharField(max_length=100, null=True, blank=True)
    unique_code = models.CharField(max_length=50, unique=True)
    company = models.ForeignKey(InsuranceCompany, on_delete=models.PROTECT)


class PolicyType(BaseModel):
    name = models.CharField(max_length=100, null=True, blank=True)
    unique_code = models.CharField(max_length=50, unique=True)


class InsurancePolicy(BaseModel):
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    accepted_date = models.DateField(null=True, blank=True)
    unique_code = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(InsuredUser, on_delete=models.PROTECT)
    company = models.ForeignKey(InsuranceCompany, on_delete=models.PROTECT)
    employer = models.ForeignKey(EmployerCompany, on_delete=models.PROTECT)
    type = models.ForeignKey(PolicyType, on_delete=models.PROTECT)
