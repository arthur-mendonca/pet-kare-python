from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = "page_pages"
    max_page_size = 10
    page_query_param = "page"
