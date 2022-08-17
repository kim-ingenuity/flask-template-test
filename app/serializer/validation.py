from flask_restplus import fields, Model

validate_serializer = {
    'duCode': fields.String(required=True),
    'accountId': fields.String(required=True)
}

#---------------------------------------------------------

error_serializer = Model('Error', {
    'flag': fields.String,
    'message': fields.String
})

validate_data_fields = Model('Vending-Validate-Data', {
    'login': fields.String,
    'du_code': fields.String,
    'account_id': fields.String
})

vending_validate_response_serializer = {
    'error': fields.Nested(error_serializer, required=True),
    'data': fields.List(fields.Nested(validate_data_fields), required=True),
    'requestDate': fields.String(required=True)
}