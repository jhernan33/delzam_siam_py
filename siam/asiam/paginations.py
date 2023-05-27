from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class SmallResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'page'
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        # response = Response(data)
        # response['count'] = self.page.paginator.count
        # response['next'] = self.get_next_link()
        # response['previous'] = self.get_previous_link()
        # return response
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'page': int(self.request.GET.get('page', 1)), # can not set default = self.page
            'page_size': int(self.request.GET.get('page_size', self.page_size)),
            'results': data
        })