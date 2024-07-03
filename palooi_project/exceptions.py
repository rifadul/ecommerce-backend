# from rest_framework.views import exception_handler
# from rest_framework.response import Response
# from rest_framework import status
# from django.core.exceptions import ObjectDoesNotExist
# from django.http import Http404
# from rest_framework.exceptions import ValidationError, NotFound, APIException

# def custom_exception_handler(exc, context):
#     # Call REST framework's default exception handler first,
#     # to get the standard error response.
#     response = exception_handler(exc, context)

#     # Custom handling for ValidationError
#     if isinstance(exc, ValidationError):
#         custom_response_data = {"message": ""}
#         for key, value in response.data.items():
#             if isinstance(value, list):
#                 custom_response_data["message"] = f"{key}: {value[0]}" if value else "An error occurred."
#             else:
#                 custom_response_data["message"] = f"{key}: {value}"
#         return Response(custom_response_data, status=status.HTTP_400_BAD_REQUEST)

#     # Custom handling for 404 errors
#     if isinstance(exc, (Http404, NotFound)):
#         return Response(
#             {"message": "The requested resource was not found."},
#             status=status.HTTP_404_NOT_FOUND
#         )

#     # Custom handling for ObjectDoesNotExist errors
#     if isinstance(exc, ObjectDoesNotExist):
#         return Response(
#             {"message": "The requested object does not exist."},
#             status=status.HTTP_404_NOT_FOUND
#         )

#     # If the response is None, it means DRF didn't handle the exception.
#     if response is None:
#         # Handle unknown endpoints and other generic API exceptions
#         if isinstance(exc, APIException):
#             return Response(
#                 {"message": exc.detail},
#                 status=exc.status_code
#             )
#         else:
#             return Response(
#                 {"message": "An unexpected error occurred. Please try again later."},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )

#     # Custom handling for other errors
#     custom_response_data = {"message": ""}
#     for key, value in response.data.items():
#         if isinstance(value, list):
#             custom_response_data["message"] = f"{key}: {value[0]}" if value else "An error occurred."
#         else:
#             custom_response_data["message"] = f"{key}: {value}"
#     response.data = custom_response_data

#     return response


# this is the code here give the error message with details

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework.exceptions import ValidationError, NotFound, APIException

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, ValidationError):
        custom_response_data = {"message": ""}
        for key, value in response.data.items():
            if isinstance(value, list):
                custom_response_data["message"] = f"{key}: {value[0]}" if value else "An error occurred."
            else:
                custom_response_data["message"] = f"{key}: {value}"
        return Response(custom_response_data, status=status.HTTP_400_BAD_REQUEST)

    if isinstance(exc, (Http404, NotFound)):
        return Response(
            {"message": "The requested resource was not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    if isinstance(exc, ObjectDoesNotExist):
        return Response(
            {"message": "The requested object does not exist."},
            status=status.HTTP_404_NOT_FOUND
        )

    if response is None:
        if isinstance(exc, APIException):
            return Response(
                {"message": exc.detail},
                status=exc.status_code
            )
        else:
            return Response(
                {"message": str(exc)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    custom_response_data = {"message": ""}
    for key, value in response.data.items():
        if isinstance(value, list):
            custom_response_data["message"] = f"{key}: {value[0]}" if value else "An error occurred."
        else:
            custom_response_data["message"] = f"{key}: {value}"
    response.data = custom_response_data

    return response