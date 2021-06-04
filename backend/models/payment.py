from db import db


class PaymentModel(db.Model):

    __tablename__ = 'payment'

    id = db.Column(db.Integer, primary_key=True)
    date_payment_efective = db.Column(db.DateTime)
    date_payment_deadline = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean)
    amount_pay = db.Column(db.Float)
    loan_id = db.Column(db.Integer, db.ForeignKey('loan.id'))

    def json(self):
        return {
            'id': self.id,
            'loan_id': self.loan_id,
            'date_payment_efective':
            (
                self.date_payment_efective.strftime('%Y-%m-%d')
                if self.date_payment_efective
                else None
            ),
            'date_payment_deadline':
            (
                self.date_payment_deadline.strftime('%Y-%m-%d')
                if self.date_payment_deadline
                else None
            ),
            'is_active': self.is_active,
            'amount_pay': self.amount_pay
        }

    def __init__(
        self, loan_id,
        date_payment_efective, date_payment_deadline,
        is_active, amount_pay
    ):
        self.loan_id = loan_id
        self.date_payment_efective = date_payment_efective
        self.date_payment_deadline = date_payment_deadline
        self.is_active = is_active
        self.amount_pay = amount_pay

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def save_many_to_db(self, data):
        db.session.add_all(data)
        db.session.commit()

    @classmethod
    def find_by_paymentid(cls, paymentid):
        return cls.query.filter_by(id=paymentid).first()
