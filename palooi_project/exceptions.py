# # updated version-02
# from rest_framework.views import exception_handler
# from rest_framework.response import Response
# from rest_framework import status
# from django.core.exceptions import ObjectDoesNotExist
# from django.http import Http404
# from rest_framework.exceptions import ValidationError, NotFound, APIException, PermissionDenied, AuthenticationFailed

# def custom_exception_handler(exc, context):
#     response = exception_handler(exc, context)

#     # Handle validation errors
#     if isinstance(exc, ValidationError):
#         custom_response_data = {
#             "message": "Validation error",
#             "errors": response.data
#         }
#         return Response(custom_response_data, status=status.HTTP_400_BAD_REQUEST)
    
#     # Handle 404 not found errors
#     if isinstance(exc, (Http404, NotFound)):
#         return Response(
#             {"message": "The requested resource was not found."},
#             status=status.HTTP_404_NOT_FOUND
#         )
    
#     # Handle object does not exist errors
#     if isinstance(exc, ObjectDoesNotExist):
#         return Response(
#             {"message": "The requested object does not exist."},
#             status=status.HTTP_404_NOT_FOUND
#         )
    
#     # Handle permission denied errors
#     if isinstance(exc, PermissionDenied):
#         return Response(
#             {"message": "You do not have permission to perform this action."},
#             status=status.HTTP_403_FORBIDDEN
#         )
    
#     # Handle authentication failed errors
#     if isinstance(exc, AuthenticationFailed):
#         return Response(
#             {"message": "Authentication credentials were not provided or are invalid."},
#             status=status.HTTP_401_UNAUTHORIZED
#         )
    
#     # Handle any other API exceptions
#     if response is None:
#         if isinstance(exc, APIException):
#             return Response(
#                 {"message": exc.detail},
#                 status=exc.status_code
#             )
#         else:
#             return Response(
#                 {"message": "An unexpected error occurred."},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )

#     # Default error handling
#     custom_response_data = {
#         "message": "An error occurred",
#         "errors": response.data
#     }
#     response.data = custom_response_data

#     return response



# this is the code here give the error message with details -updated version-01

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework.exceptions import ValidationError, NotFound, APIException
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

def custom_exception_handler(exc, context):
    # Call the default exception handler to get the standard error response
    response = exception_handler(exc, context)

    # Handle JWT token errors
    if isinstance(exc, (TokenError, InvalidToken)):
        return Response(
            {"message": "Your session has expired or the token is invalid. Please log in again."},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # Handle validation errors
    if isinstance(exc, ValidationError):
        custom_response_data = {"message": ""}
        for key, value in response.data.items():
            if isinstance(value, list):
                custom_response_data["message"] = f"{key}: {value[0]}" if value else "An error occurred."
            else:
                custom_response_data["message"] = f"{key}: {value}"
        return Response(custom_response_data, status=status.HTTP_400_BAD_REQUEST)

    # Handle 404 errors
    if isinstance(exc, (Http404, NotFound)):
        return Response(
            {"message": "The requested resource was not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    # Handle object not found errors
    if isinstance(exc, ObjectDoesNotExist):
        return Response(
            {"message": "The requested object does not exist."},
            status=status.HTTP_404_NOT_FOUND
        )

    # Handle generic API exceptions
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

    # Customize the default error response
    custom_response_data = {"message": ""}
    for key, value in response.data.items():
        if isinstance(value, list):
            custom_response_data["message"] = f"{key}: {value[0]}" if value else "An error occurred."
        else:
            custom_response_data["message"] = f"{key}: {value}"
    response.data = custom_response_data

    return response




# updated version-00.0
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

