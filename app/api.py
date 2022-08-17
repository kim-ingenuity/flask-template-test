from http import HTTPStatus
# import resource

from flask import Blueprint
from flask_restplus import Resource, Api

from sqlalchemy.exc import DatabaseError
from werkzeug.exceptions import BadRequest, NotFound

from core.main import PatchedApi as Api

from app.resources.test import test
from app.resources.validation import api_vending_validation 


blueprint = Blueprint('flask_api', __name__)
api = Api(
    blueprint,
    version='1.0',
    prefix='/api',
    title='Flask',
    description='Flask API'
)



@blueprint.route('/health', methods=['GET'])
def health_check():
    """
    Endpoint for checking health status of API. Additional health check conditions
    can be added here in order to further assess the status of the API.
    """
    data = {'healthy': True}

    return data, HTTPStatus.OK


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

api.add_namespace(test, path='/app')
api.add_namespace(api_vending_validation, path='/app')
# api.add_namespace(health_check)

if __name__ == '__main__':
    api.run(debug=True)
