from django.core.management.base import BaseCommand
from ...models import (
    InsuranceCompany,
    EmployerCompany,
    PolicyType,
)


class Command(BaseCommand):
    help = "Create initial insurance-related data"

    def handle(self, *args, **kwargs):
        data = {
            "InsuranceCompany": {"name": "saman", "unique_code": "123"},
            "EmployerCompany": {
                "name": "Shahrzaad Co",
                "unique_code": "456",
                "company": "123",
            },
            "PolicyType": {"name": "Life Insurance", "unique_code": "2024"},
        }

        insurance_company, _ = InsuranceCompany.objects.get_or_create(
            unique_code=data["InsuranceCompany"]["unique_code"],
            defaults={"name": data["InsuranceCompany"]["name"]},
        )

        employer_company, _ = EmployerCompany.objects.get_or_create(
            unique_code=data["EmployerCompany"]["unique_code"],
            defaults={
                "name": data["EmployerCompany"]["name"],
                "company": insurance_company,
            },
        )

        policy_type, _ = PolicyType.objects.get_or_create(
            unique_code=data["PolicyType"]["unique_code"],
            defaults={"name": data["PolicyType"]["name"]},
        )

        self.stdout.write(self.style.SUCCESS("Insurance data created successfully."))
