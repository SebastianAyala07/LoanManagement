from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from resources.user import UserRegister, UserList
from resources.state import State, StateList
from resources.loan import Loan
from resources.payment import Payment,PaymentMasiv

from security import authenticate, identity
from initial_data import InitialInformation

from db import db
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQL_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ['SECRET_API_KEY']
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()
    InitialInformation.create_inital_data(db)

jwt = JWT(app, authenticate, identity)

api.add_resource(UserRegister, '/api/user/register')
api.add_resource(State, '/api/state')
api.add_resource(StateList, '/api/states')
api.add_resource(UserList, '/api/admin/users')
api.add_resource(Loan, '/api/loan')
api.add_resource(Payment, '/api/payment')
api.add_resource(PaymentMasiv, '/api/payments/generate')


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
