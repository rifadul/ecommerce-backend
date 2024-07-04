from rest_framework.pagination import PageNumberPagination

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10  # Default page size
    page_size_query_param = 'page_size'  # Query parameter to override the default page size
    max_page_size = 100  # Maximum page size allowed

    def get_page_size(self, request):
        if 'page_size' in request.query_params:
            return int(request.query_params['page_size'])
        return self.page_size
