from rest_framework.pagination import PageNumberPagination


class CustumPagination(PageNumberPagination):
    page_size_query_param = 'limit'
