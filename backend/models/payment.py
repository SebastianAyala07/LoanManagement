from db import db


class Payment(db.Model):

    __tablename__ = 'paymnet'

    id = db.Column(db.Integer, primary_key=True)
    date_payment_efective = db.Column(db.Date)
    date_payment_deadline = db.Column(db.Date)
    is_active = db.Column(db.Boolean)
    amount_pay = db.Column(db.Float)

    def json(self):
        return {
            'id': self.id,
            'date_payment_efective': self.date_payment_efective,
            'date_payment_deadline': self.date_payment_deadline,
            'is_active': self.is_active,
            'amount_pay': self.amount_pay
        }

    def __init__(
        self,
        date_payment_efective, date_payment_deadline,
        is_active, amount_pay
    ):
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
    def find_by_paymentid(cls, paymentid):
        return cls.query.filter_by(id=paymentid).first()
