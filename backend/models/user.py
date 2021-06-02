from db import db


class UserModel(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150))
    password = db.Column(db.String(80))

    loans = db.relationship('LoanModel', lazy='dynamic')

    def json(self):
        return {
            'id': self.id,
            'email': self.email,
            'password': self.password,
            'loans': list(
                map(
                    lambda x: x.json(), self.loans.all()
                )
            )
        }

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_userid(cls, userid):
        return cls.query.filter_by(id=userid)
