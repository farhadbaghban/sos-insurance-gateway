from .base import BaseHandler
from ..schema.base import get_dynamic_schema_for_serializer

from ..serializers.serializers import generate_serializer_class
from ..schema.utils import map_and_validate_input
from ..insurance_processing.step_insurance_processor import StepInsuranceProcessor
from rest_framework.exceptions import ValidationError


class SamanHandler(BaseHandler):
    def parse(self):
        try:
            self.field_map, self.category_list = get_dynamic_schema_for_serializer(
                schema_name="saman"
            )
            self.serializer_class = generate_serializer_class(field_map=self.field_map)
            map_and_validate_input(self.field_map, self.raw_data)
            self.serializer = self.serializer_class(data=self.raw_data)
            self.serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            raise e
        except Exception as e:
            raise ValidationError({"non_field_error in Saman Handler": str(e)})

    def save(self):
        return StepInsuranceProcessor(
            self.serializer.validated_data, self.category_list
        ).process()
