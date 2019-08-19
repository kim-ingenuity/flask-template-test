from http import HTTPStatus

from flask import Blueprint

from sqlalchemy.exc import DatabaseError
from werkzeug.exceptions import BadRequest, NotFound

from core.main import PatchedApi as Api


blueprint = Blueprint('flask_api', __name__)
api = Api(
    blueprint,
    version='1.0',
    prefix='/api/v1',
    title='Flask',
    description='Flask API'
)


@api.errorhandler(ValueError)
def handle_value_errors(error):
    """Returns a 400 and the specific message for ValueErrors."""
    return {
        'status': HTTPStatus.BAD_REQUEST,
        'message': 'A ValueError has occurred',
        'error': str(error)
    }, HTTPStatus.BAD_REQUEST


@api.errorhandler(KeyError)
def handle_value_errors(error):
    """Returns a 400 and the specific message for ValueErrors."""
    return {
        'status': HTTPStatus.BAD_REQUEST,
        'message': 'A KeyError has occurred',
        'error': str(error)
    }, HTTPStatus.BAD_REQUEST


@api.errorhandler(DatabaseError)
def handle_database_errors(error):
    """
    Returns a 500 if the DatabaseError is related to failing database connection.

    Returns 400 and a custom message for everything else.
    """
    split_error_list = str(error).split(' ')
    if 'ORA-12541:' in split_error_list or 'ORA-12537:' in split_error_list:
        return {
            'status': HTTPStatus.INTERNAL_SERVER_ERROR,
            'message': 'An error occurred with the database connection',
            'error': str(error)
        }, HTTPStatus.INTERNAL_SERVER_ERROR

    return {
        'status': HTTPStatus.BAD_REQUEST,
        'message': 'An error occurred with the database',
        'error': str(error) or HTTPStatus.BAD_REQUEST.description
    }, HTTPStatus.BAD_REQUEST


@api.errorhandler(BadRequest)
def handle_bad_request_errors(error):
    """
    Returns 400 and a custom message.

    Default message is 'Bad request syntax or unsupported method'
    """
    detail = None
    if hasattr(error, 'detail'):
        detail = error.detail

    return {
        'status': HTTPStatus.BAD_REQUEST,
        'message': str(error.description) or HTTPStatus.BAD_REQUEST.description,
        'error': detail or error.description
    }, HTTPStatus.BAD_REQUEST


@api.errorhandler(NotFound)
def handle_not_found_errors(error):
    """
    Returns 400 and a custom message.

    Default message is 'Bad request syntax or unsupported method'
    """
    detail = None
    if hasattr(error, 'detail'):
        detail = error.detail

    return {
        'status': HTTPStatus.NOT_FOUND,
        'message': str(error.description) or HTTPStatus.NOT_FOUND.description,
        'error': detail or error.description
    }, HTTPStatus.NOT_FOUND


@api.errorhandler
def handle_all_other_errors(error):
    """
    Returns 500 and custom message.

    Default message is 'An unexpected error occured.'
    """
    detail = None
    if hasattr(error, 'detail'):
        detail = error.detail

    return {
        'status': HTTPStatus.INTERNAL_SERVER_ERROR,
        'message': str(error) or 'An unexpected error occured.',
        'error': detail or error.description
    }, HTTPStatus.INTERNAL_SERVER_ERROR


# ADD NAMESPACES HERE
# e.g. api.add_namespace(api_hello path='/hello')


if __name__ == '__main__':
    api.run(debug=True)
