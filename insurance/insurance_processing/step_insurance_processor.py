from django.db import transaction
from rest_framework.exceptions import ValidationError
from ..models import (
    InsuranceCompany,
    InsurancePolicy,
    InsuredUser,
    PolicyType,
    EmployerCompany,
)


class StepInsuranceProcessor:
    def __init__(self, validated_data, category_list):
        self.validated_data = validated_data
        self.errors = {}

    @transaction.atomic
    def process(self):
        try:
            self._get_or_create_user()
            self._get_or_create_company()
            self._get_or_create_employer()
            self._get_or_create_policy_type()
            self._create_policy()
        except ValidationError as e:
            raise e
        except Exception as e:
            raise ValidationError({"non_field_error": str(e)})

    def _get_or_create_user(self):
        user_data = self.validated_data.get("user")
        try:
            self.user = InsuredUser.objects.get(id_card_number=user_data.id_card_number)
        except InsuredUser.DoesNotExist:
            self.user = InsuredUser.objects.create(**user_data)

    def _get_or_create_company(self):
        company_data = self.validated_data.get("company")
        try:
            self.company = InsuranceCompany.objects.get(name=company_data["name"])
            if self.company.unique_code != company_data["unique_code"]:
                raise ValidationError(
                    {"unique_code": "unique code in company data is not match."}
                )
        except InsuranceCompany.DoesNotExist:
            self.company = InsuranceCompany.objects.create(**company_data)

    def _get_or_create_employer(self):
        employer_data = self.validated_data.get("employer")
        try:
            self.employer = EmployerCompany.objects.get(
                name=employer_data["name"], company=employer_data["company"]
            )
            if self.employer.unique_code != employer_data["unique_code"]:
                raise ValidationError(
                    {"unique_code": "unique code in employee data is not match."}
                )

        except EmployerCompany.DoesNotExist:
            self.employer = EmployerCompany.objects.create(**employer_data)

    def _get_or_create_policy_type(self):
        policy_data = self.validated_data.get("policy_type")
        try:
            self.policy_type = PolicyType.objects.get(name=policy_data["name"])
            if self.policy_type.unique_code != policy_data["unique_code"]:
                raise ValidationError(
                    {"unique_code": "unique code in policy type data is not match."}
                )
        except PolicyType.DoesNotExist:
            self.policy_type = PolicyType.objects.create(**policy_data)

    def _create_policy(self):
        policy_data = self.validated_data["policy"]
        self.policy = InsurancePolicy.objects.create(
            user=self.user,
            company=self.company,
            employer=self.employer,
            type=self.policy_type,
            start_time=policy_data["start_time"],
            end_time=policy_data["end_time"],
            accepted_date=policy_data["accepted_date"],
        )
