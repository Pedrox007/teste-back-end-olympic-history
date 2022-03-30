from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class FilterPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = "page_size"

    def get_paginated_response(self, data):
        return Response(
            {
                "links": {"next": self.get_next_link(), "previous": self.get_previous_link()},
                "count": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "results": data,
            }
        )