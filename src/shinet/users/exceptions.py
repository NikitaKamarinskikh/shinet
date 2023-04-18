from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError
from rest_framework.status import HTTP_422_UNPROCESSABLE_ENTITY


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.status_code = HTTP_422_UNPROCESSABLE_ENTITY
        if isinstance(exc, ValidationError):
            error_list = []
            for field, errors in exc.detail.items():
                for error in errors:
                    error_list.append({
                        'field': field,
                        'message': error
                    })
            response.data = {
                'errors': error_list
            }
    return response


