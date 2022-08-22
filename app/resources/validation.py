import json
import sys
from http import HTTPStatus
from datetime import datetime

from flask_restplus import Namespace, Resource
from flask import request
from sqlalchemy import func

from app.models.validation import PrepaidAccountObj
from app.serializer.validation import validate_serializer, vending_validate_response_serializer

from core.settings import Config

VENDING_ROOT_PATH = '/vending'
api_vending_validation = Namespace('Vending: Validation', path=VENDING_ROOT_PATH)

validate_response = api_vending_validation.model('Vending-Validate-Response', vending_validate_response_serializer)
validate_fields = api_vending_validation.model('Vending-Validate', validate_serializer)

@api_vending_validation.route('/validate-account')
class AccountValidation(Resource):

    @api_vending_validation.marshal_with(
        validate_response,
        description='Vending: Validate Account'
    )
    @api_vending_validation.expect(validate_fields, validate=True)
    @api_vending_validation.doc(responses={400: 'Bad Request', 500: 'Internal Server Error'})
    # @token_required
    def post(self, **kwargs):

        req_data = {
            # 'login': None,
            'du_code': None,
            'account_id': None,

        }
        response_data = {
            'error': {
                'flag': False,
                'message': 'OK'
            },
            'data': [],
            'requestDate': datetime.now(Config.tz).strftime("%m/%d/%Y")
        }

        data = json.loads(request.data)
        client_id = data.get('ServiceClient', 'None')
        client_version = data.get('ServiceVersion', '1')
        status = HTTPStatus.OK

        try:

            # user = kwargs.get('user')
            # login = user.username
            account_id = data.get('accountId')
            du_code = data.get('duCode')

            # req_data['login'] = login
            req_data['du_code'] = du_code
            req_data['account_id'] = account_id

            if du_code.lower() != Config.DU_CODE.lower():
                status = HTTPStatus.BAD_REQUEST
                response_data['error']['flag'] = True
                response_data['error']['message'] = 'Invalid DU code.'
            elif not account_id.isnumeric():
                status = HTTPStatus.BAD_REQUEST
                response_data['error']['flag'] = True
                response_data['error']['message'] = 'Invalid account ID.'
            elif len(account_id) > 11 or len(account_id) < 10:
                status = HTTPStatus.BAD_REQUEST
                response_data['error']['flag'] = True
                response_data['error']['message'] = 'Invalid account ID.'
            elif len(account_id) == 11:
                # check = check_digit(account_id)
                check = True
                if check:
                    account_id = account_id[:10]
                    account = PrepaidAccountObj.query.filter(
                        func.lower(PrepaidAccountObj.du_code) == du_code.lower()
                    ).filter_by(
                        acct_id=account_id,
                        status='ACTIVE'
                    ).first()

                    if not account:
                        status = HTTPStatus.BAD_REQUEST
                        response_data['error']['flag'] = True
                        response_data['error']['message'] = 'Account does not exist.'

                else:
                    status = HTTPStatus.BAD_REQUEST
                    response_data['error']['flag'] = True
                    response_data['error']['message'] = 'Invalid account ID.'

            else:
                account = PrepaidAccountObj.query.filter(
                    func.lower(PrepaidAccountObj.du_code) == du_code.lower()
                ).filter_by(
                    acct_id=account_id,
                    status='ACTIVE'
                ).first()

                if not account:
                    status = HTTPStatus.BAD_REQUEST
                    response_data['error']['flag'] = True
                    response_data['error']['message'] = 'Account does not exist.'

            response_data['data'] = req_data
            return response_data, status

        except Exception as e:
            response_data['error']['flag'] = True
            response_data['error']['message'] = f"Invalid incident code: {sys.exc_info()[-1].tb_lineno, type(e).__name__, e}"

            # ErrorLog.create(**{
            #     'process_type_id': 'vending',
            #     'created_at': datetime.now(Config.tz),
            #     'error_code': 500,
            #     'error_msg': f"Invalid incident code: {sys.exc_info()[-1].tb_lineno, type(e).__name__, e}",
            #     'client_id': client_id,
            #     'client_version': client_version
            # })

            return response_data, HTTPStatus.INTERNAL_SERVER_ERROR