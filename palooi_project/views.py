from django.http import JsonResponse

def custom_404_view(request, exception=None):
    return JsonResponse(
        {"detail": "The requested resource was not found."},
        status=404
    )

def custom_500_view(request):
    return JsonResponse(
        {"detail": "An internal server error occurred."},
        status=500
    )