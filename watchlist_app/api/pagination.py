from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

class WatchListPagination(PageNumberPagination):
    page_size = '5'
    page_query_param = 'records'
    page_size_query_param = 'size' # to overwrite  page_size directly in the url // /?page=5&size=10
    max_page_size = '10'
    # last_page_strings = 'end' #/?p=end

class WatchListOPagination(LimitOffsetPagination): #/?limit=5&offset=10 (we will skip first 10 elements)
    default_limit = 5

class WatchListCPagination(CursorPagination): #this order by date i have to get a date field in my data base
    page_size = 5
    ordering = '-created'
    # cursor_query_param = ''
