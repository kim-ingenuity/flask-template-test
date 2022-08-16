from flask_restplus import Namespace, Resource
from app.serializer.test import test_field

from http import HTTPStatus

test = Namespace('test', description='test endpoint')
test_response = test.model('Test-Response', test_field)

@test.route('/test')
class TestResource(Resource):

    @test.marshal_with(
        test_response,
        description = 'Test Endpoint'
    )
    @test.expect()
    @test.doc(response = {400: 'Bad Request', 500: 'Internal Server Error'})
    def get(self):
        
        world = 'World'

        response_data = {
            'Hello' : world
        }

        return response_data, HTTPStatus.OK