from django.http import JsonResponse
from rest_framework.pagination import PageNumberPagination


class FilterPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = "page_size"

    def get_paginated_response(self, data):
        return JsonResponse(
            {
                "links": {"next": self.get_next_link(), "previous": self.get_previous_link()},
                "count": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "results": data,
            }
        )