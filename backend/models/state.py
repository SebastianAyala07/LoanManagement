from db import db


class StateModel(db.Model):

    __tablename__ = 'state'
    __table_args__ = (
        db.UniqueConstraint('code', name='unique_state_code_constraint'),
    )

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20))
    description = db.Column(db.String(50))
    apply_for_loan = db.Column(db.Boolean)

    def json(self):
        return {
            'id': self.id,
            'code': self.code,
            'description': self.description,
            'apply_for_loan': self.apply_for_loan
        }

    def __init__(self, code, description, apply_for_loan):
        self.code = code
        self.description = description
        self.apply_for_loan = apply_for_loan

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_code(cls, code):
        return cls.query.filter_by(code=code).first()

    @classmethod
    def find_by_stateid(cls, stateid):
        return cls.query.filter_by(id=stateid).first()
