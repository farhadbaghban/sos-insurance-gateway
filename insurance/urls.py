from django.urls import path
from .views import InsuranceDataReceiverView

app_name = "insurance"

urlpatterns = [
    path(
        "api/v1/receive/",
        InsuranceDataReceiverView.as_view(),
        name="company-data-receiver",
    ),
]
