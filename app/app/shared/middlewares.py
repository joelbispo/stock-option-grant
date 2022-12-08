from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def pretty_exception_handler(exc, context) -> Response:
    """ Pretty exception handler."""
    response = exception_handler(exc, context)

    if response is not None:
        response.data['status_code'] = status.HTTP_400_BAD_REQUEST

    return response
