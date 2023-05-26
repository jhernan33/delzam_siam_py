from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class SmallResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'page'
    page_size_query_param = 'page_size'

    # def get_paginated_response(self, data):
    #     response = Response(data)
    #     response['count'] = self.page.paginator.count
    #     response['next'] = self.get_next_link()
    #     response['previous'] = self.get_previous_link()
    #     return response