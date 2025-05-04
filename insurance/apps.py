from django.apps import AppConfig


class InsuranceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "insurance"

    def ready(self):
        from .handlers.saman import SamanHandler
        from .handlers.base import CompanyHandlerFactory

        CompanyHandlerFactory.register_handler("saman", SamanHandler)
