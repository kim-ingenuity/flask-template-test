from flask_restplus import fields, Model

test_field = Model('test-fields', {
    'Hello': fields.String
})