from flask_restplus.reqparse import RequestParser

from werkzeug.exceptions import BadRequest, NotFound

from core.settings import Config


class Pagination:
    """
    TO BE DEPRECATED IN FAVOR OF QueryPagination

    A simple pagination class.

    Returns the paginated results of a given list using the request query parameters
    'pageSize' and 'pageNumber'.
    """
    parser = None

    def __init__(self, page_size_help='objects'):
        self.parser = RequestParser()
        self.setup(page_size_help)

    def setup(self, page_size_help='objects'):
        """Pagination setup method"""
        self.parser.add_argument(
            'pageSize',
            type=int,
            help=f'Number of {page_size_help} returned'
        )
        self.parser.add_argument(
            'pageNumber',
            type=int,
            help='Page number'
        )

    def get_args(self):
        """Returns the pagination query parameters"""
        return self.parser.parse_args()

    def get_parser(self):
        """Returns the pagination RequestParser"""
        return self.parser

    def get_paginated_response(self, data):
        """
        Returns the paginated data according to the request parameters.

        If page size isn't provided, the DEFAULT_PAGINATION_SIZE will be used.

        A BadRequest exception will be raised if the page number exceeds the
        actual maximum number of pages.
        """
        params = self.get_args()
        start = 0
        end = None

        if params['pageNumber']:
            size = params['pageSize']
            if not size:
                size = Config.DEFAULT_PAGINATION_SIZE

            start = size * (params['pageNumber'] - 1)
            end = start + size

        if start > len(data):
            raise BadRequest(
                "'pageNumber' parameter exceeds the actual maximum pages")
        if end and end > len(data):
            end = None

        return data[start:end]


class QueryPagination:
    """
    A query pagination class.

    Returns the paginated queryset of the given model and query using the request
    query parameters 'pageSize' and 'pageNumber'.
    """
    parser = None
    model = None

    def __init__(self, model=None, page_size_help='objects'):
        self.parser = RequestParser()
        self.model = model
        self.setup(page_size_help)

    def setup(self, page_size_help='objects'):
        """QueryPagination setup method"""
        self.parser.add_argument(
            'pageSize',
            type=int,
            help=f'Number of {page_size_help} returned'
        )
        self.parser.add_argument(
            'pageNumber',
            type=int,
            help='Page number'
        )

    def get_args(self):
        """Returns the pagination query parameters"""
        return self.parser.parse_args()

    def get_parser(self):
        """Returns the pagination RequestParser"""
        return self.parser

    def get_paginated_queryset(self, query={}):
        """
        Returns the paginated queryset according to the request parameters.

        If page size isn't provided but a page number was provided, the
        DEFAULT_PAGINATION_SIZE will be used.

        A BadRequest exception will be raised if the page number exceeds the
        actual maximum number of pages.
        """
        params = self.get_args()
        size = params['pageSize']
        data = []

        if params['pageNumber'] and not size:
            size = Config.DEFAULT_PAGINATION_SIZE

        try:
            if not query:
                data = self.model.query.paginate(
                    params['pageNumber'], size).items
            else:
                data = self.model.query.filter_by(
                    **query).paginate(params['pageNumber'], size).items
        except NotFound as err:
            raise BadRequest(
                "'pageNumber' parameter exceeds the actual maximum pages")

        return data
