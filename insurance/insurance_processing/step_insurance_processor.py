from typing import Type, Optional
from django.db.models import Model
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
            raise ValidationError({"non_field_error in StepInsuranceProcessor": str(e)})

    def _get_or_create_user(self, id_card_number: str = None):
        if id_card_number:
            return InsuredUser.objects.filter(id_card_number=id_card_number).first()
        self.user = InsuredUser.objects.filter(
            id_card_number=self.validated_data["InsuredUser"]["id_card_number"]
        ).first()
        if not self.user:
            self.user = self._create_instance(InsuredUser)
        return self.user

    def _get_or_create_company(self, company_unique_code: int = None):
        self.company = self._get_instance(InsuranceCompany, company_unique_code)
        if self.company is None:
            if company_unique_code:
                return None
            self.company = self._create_instance(InsuranceCompany)
        else:
            if company_unique_code:
                return self.company
            if self.company.name != self.validated_data["InsuranceCompany"]["name"]:
                raise ValidationError(
                    {"unique_code": "unique code in company data is not match."}
                )
        return self.company

    def _get_or_create_employer(self, employer_unique_code: int = None):
        employer_data = self.validated_data.get("EmployerCompany")

        company = self._get_or_create_company(employer_data["company"])
        self.employer = self._get_instance(EmployerCompany, employer_unique_code)
        if self.employer is None:
            if employer_unique_code:
                return None
            self.employer = EmployerCompany.objects.create(
                name=employer_data["name"],
                unique_code=employer_data["unique_code"],
                company=company,
            )
        else:
            if self.employer.company.unique_code == company.unique_code:
                if employer_unique_code:
                    return self.employer
            else:
                raise ValidationError(
                    {
                        "unique_code": "company unique code  data is not match in employer data."
                    }
                )

        return self.employer

    def _get_or_create_policy_type(self, policy_unique_code: int = None):
        self.policy_type = self._get_instance(PolicyType, policy_unique_code)

        if self.policy_type is None:
            if policy_unique_code:
                return None
            self.policy_type = self._create_instance(PolicyType)
        else:
            if policy_unique_code:
                return self.policy_type
            if self.policy_type.name != self.validated_data["PolicyType"]["name"]:
                raise ValidationError(
                    {"unique_code": "unique code in policy  data is not match."}
                )

        return self.policy_type

    def _create_policy(self):
        policy_data = self.validated_data["InsurancePolicy"]
        self.policy = InsurancePolicy.objects.create(
            user=self.user,
            company=self.company,
            employer=self.employer,
            type=self.policy_type,
            start_time=policy_data["start_time"],
            end_time=policy_data["end_time"],
            accepted_date=policy_data["accepted_date"],
        )

    def _get_instance(
        self, model_class: Type[Model], unique_field: Optional[int] = None
    ) -> Optional[Model]:
        if not unique_field:
            valid_data = self.validated_data.get(model_class.__name__)
            unique_field = valid_data["unique_code"]
        data = model_class.objects.filter(unique_code=unique_field).first()
        return data

    def _create_instance(self, model_class: Type[Model]) -> Model:
        valid_data = self.validated_data.get(model_class.__name__)
        record = model_class.objects.create(**valid_data)
        return record
