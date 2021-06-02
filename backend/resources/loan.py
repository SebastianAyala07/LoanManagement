from flask_restful import Resource, reqparse, inputs
from flask_jwt import jwt_required, current_identity
from models.loan import LoanModel
from models.state import StateModel

from datetime import date


class Loan(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'fiscal_number',
        required=True,
        type=str,
        help="This field cannot be left blank!"
    )
    parser.add_argument(
        'company_name',
        required=True,
        type=str,
        help="This field cannot be left blank!"
    )
    parser.add_argument(
        'amount_money',
        required=True,
        type=inputs.positive,
        help="This field cannot be left blank and not can be negative or zero!"
    )
    parser.add_argument(
        'is_loan',
        required=True,
        type=inputs.boolean,
        help="This field cannot be left blank!"
    )
    parser.add_argument(
        'number_installments',
        required=True,
        type=int,
        help="This field cannot be left blank!"
    )

    def get(self):
        parser_get = reqparse.RequestParser()
        parser_get.add_argument(
            'id',
            required=True,
            type=int,
            help="This field cannot be left blank!"
        )
        data = parser_get.parse_args()
        loan = LoanModel.find_by_loanid(data['id'])
        if loan:
            return loan.json()
        return {'message': 'Loan not found'}, 404

    @jwt_required()
    def post(self):
        data = Loan.parser.parse_args()
        user = current_identity.first()
        loan = LoanModel(
            user.id,
            1,
            data['fiscal_number'],
            data['company_name'],
            data['amount_money'],
            data['is_loan'],
            number_installments=data['number_installments']
        )
        loan.save_to_db()
        return loan.json(), 201

    def put(self):
        parser_put = self.parser
        parser_put.add_argument(
            'id',
            required=True,
            type=int,
            help="This field cannot be left blank!"
        )
        parser_put.add_argument(
            'accept_terms_conditions',
            required=True,
            type=inputs.boolean,
            help="This field cannot be left blank!"
        )
        parser_put.add_argument(
            'missing_debt',
            required=True,
            type=float,
            help="This field cannot be left blank!"
        )
        parser_put.add_argument(
            'date_response',
            required=True,
            type=inputs.date,
            help="This field cannot be left blank!"
        )
        data = parser_put.parse_args()
        user = current_identity.first()
        loan = LoanModel.find_by_loanid(data['id'])
        if loan is None:
            loan = LoanModel(
                user.id, data['fiscal_number'], data['company_name'],
                data['amount_money'], data['is_loan'],
                data['accept_terms_conditions'], data['missing_debt'],
                data['number_installments'], data['date_response']
            )
        else:
            loan.fiscal_number = data['fiscal_number']
            loan.company_name = data['company_name']
            loan.amount_money = data['amount_money']
            loan.is_loan = data['is_loan']
            loan.accept_terms_conditions = data['accept_terms_conditions']
            loan.missing_debt = data['missing_debt'],
            loan.number_installments = data['number_installments']
            loan.date_response = data['date_response']
        loan.save_to_db()
        return loan.json()

    def delete(self):
        parser_delete = reqparse.RequestParser()
        parser_delete.add_argument(
            'id',
            required=True,
            type=int,
            help="This field cannot be left blank!"
        )
        data = parser_delete.parse_args()
        loan = LoanModel.find_by_loanid(data['id'])
        if loan:
            loan.delete_from_db()
            return {'message': 'Loan deleted'}
        return {'message': 'Loan no exists'}, 400
