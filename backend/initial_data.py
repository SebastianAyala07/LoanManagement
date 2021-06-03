from models.state import StateModel


INITIAL_STATES = {
    'default': {
        'code': 'PND',
        'description': 'Pending',
        'apply_for_loan': False
    },
    'approved': {
        'code': 'APPR',
        'description': 'Approved',
        'apply_for_loan': False
    },
    'denied': {
        'code': 'DND',
        'description': 'Denied',
        'apply_for_loan': False
    },
    'active': {
        'code': 'ACT',
        'description': 'Active',
        'apply_for_loan': True
    },
    'closed': {
        'code': 'CLS',
        'description': 'Closed',
        'apply_for_loan': True
    }
}


class InitialInformation():

    @classmethod
    def create_inital_data(cls, db):
        if len(db.session.query(StateModel).all()) == 0:
            for state in INITIAL_STATES.values():
                db.session.add(
                    StateModel(
                        state.get('code'),
                        state.get('description'),
                        state.get('apply_for_loan')
                    )
                )
            db.session.commit()
