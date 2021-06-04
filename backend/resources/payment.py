from flask_restful import Resource, reqparse, inputs
from models.payment import PaymentModel
from models.loan import LoanModel

from datetime import timedelta


class Payment(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'loan_id',
        required=True,
        type=int,
        help="This field cannot be left blank!"
    )
    parser.add_argument(
        'date_payment_efective',
        required=True,
        type=inputs.date,
        help="This field cannot be left blank!"
    )
    parser.add_argument(
        'date_payment_deadline',
        required=True,
        type=inputs.date,
        help="This field cannot be left blank!"
    )
    parser.add_argument(
        'is_active',
        required=True,
        type=inputs.boolean,
        help="This field cannot be left blank!"
    )
    parser.add_argument(
        'amount_pay',
        required=True,
        type=inputs.positive
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
        payment = PaymentModel.find_by_paymentid(data['id'])
        if payment:
            return payment.json()
        return {'message': 'Payment not found'}, 404

    def post(self):
        data = Payment.parser.parse_args()
        payment = PaymentModel(
            data['loan_id'],
            data['date_payment_efective'],
            data['date_payment_deadline'],
            data['is_active'],
            data['amount_pay']
        )
        payment.save_to_db()
        return payment.json(), 201

    def put(self):
        parser_put = self.parser
        parser_put.add_argument(
            'id',
            required=True,
            type=int,
            help="This field cannot be left blank!"
        )
        data = parser_put.parse_args()
        payment = PaymentModel.find_by_paymentid(data['id'])
        if payment is None:
            payment = PaymentModel(
                data['loan_id'],
                data['date_payment_efective'],
                data['date_payment_deadline'],
                data['is_active'],
                data['amount_pay'],
            )
        else:
            payment.date_payment_efective = data['date_payment_efective']
            payment.date_payment_deadline = data['date_payment_deadline']
            payment.is_active = data['is_active']
            payment.amount_pay = data['amount_pay']
        payment.save_to_db()
        return payment.json()

    def delete(self):
        parser_delete = reqparse.RequestParser()
        parser_delete.add_argument(
            'id',
            required=True,
            type=int,
            help="This field cannot be left blank!"
        )
        data = parser_delete.parse_args()
        payment = PaymentModel.find_by_paymentid(data['id'])
        if payment:
            payment.delete_from_db()
            return {'message': 'Payment deleted'}
        return {'message': 'Payment no exists'}, 400


class PaymentMasiv(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'loan_id',
        required=True,
        type=int,
        help="This field cannot be left blank!"
    )

    def post(self):
        data = self.parser.parse_args()
        loan = LoanModel.find_by_loanid(data['loan_id'])
        if loan is None:
            return {'message': 'Loan not found'}, 400
        elif not (loan.is_loan and loan.accept_terms_conditions):
            return {'message': 'Unable to generate payments for a loan application'}, 400
        amount_per_day = loan.amount_money / loan.number_installments
        date_to_pay = loan.date_response + timedelta(days=1)
        payments_to_create = list()
        for i in range(loan.number_installments):
            payment_daily = PaymentModel(
                loan.id,
                None,
                date_to_pay,
                True, # Active is true if it has not yet been paid
                amount_per_day
            )
            payments_to_create.append(payment_daily)
            date_to_pay += timedelta(days=1)
        pay = PaymentModel.save_many_to_db(payments_to_create)
        return {'payments': list(map(lambda x: x.json(), payments_to_create))}, 201
