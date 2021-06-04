from db import db


class LoanModel(db.Model):

    __tablename__ = 'loan'

    id = db.Column(db.Integer, primary_key=True)
    fiscal_number = db.Column(db.String(50))
    company_name  = db.Column(db.String(100))
    amount_money = db.Column(db.Float)
    accept_terms_conditions = db.Column(db.Boolean)
    is_loan = db.Column(db.Boolean)
    missing_debt = db.Column(db.Float)
    number_installments = db.Column(db.Integer)
    date_response = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'))

    payments = db.relationship('PaymentModel', lazy='dynamic')

    def json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'state_id': self.state_id,
            'fiscal_number': self.fiscal_number,
            'company_name': self.company_name,
            'amount_money': self.amount_money,
            'accept_terms_conditions': self.accept_terms_conditions,
            'is_loan': self.is_loan,
            'missing_debt': self.missing_debt,
            'number_installments': self.number_installments,
            'date_response':
            (
                self.date_response.strftime('%Y-%m-%d')
                if self.date_response
                else None
            ),
            'payments': list(
                map(
                    lambda x: x.json(), self.payments.all()
                )
            )
        }

    def __init__(
        self, user_id, state_id, fiscal_number, company_name, amount_money,
        is_loan, accept_terms_conditions=False, missing_debt=0,
        number_installments=0, date_response=None
    ):
        self.user_id = user_id
        self.state_id = state_id
        self.fiscal_number = fiscal_number
        self.company_name = company_name
        self.amount_money = amount_money
        self.accept_terms_conditions = accept_terms_conditions
        self.is_loan = is_loan
        self.missing_debt = missing_debt
        self.number_installments = number_installments
        self.date_response = date_response

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_loanid(cls, loanid):
        return cls.query.filter_by(id=loanid).first()
