from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .handlers.base import CompanyHandlerFactory
from rest_framework.exceptions import ValidationError


class InsuranceDataReceiverView(APIView):
    def post(self, request):
        company_id = request.headers.get("X-Company-ID")
        if not company_id:
            return Response(
                {"error": "Missing 'X-Company-ID' header."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            handler_class = CompanyHandlerFactory.get_handler(company_id)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            handler = handler_class(request.data)
            handler.parse()
            handler.save()
            return Response(
                {"detail": "Data saved successfully."}, status=status.HTTP_201_CREATED
            )
        except ValidationError as e:
            return Response(
                {"validation_error": e.detail}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": f"Unexpected error occurred: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
