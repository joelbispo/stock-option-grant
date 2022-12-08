from rest_framework.exceptions import APIException


class BusinessValidationError(APIException):
    status_code = 400
    default_detail = "Validation error."
    default_code = "validation_error"
