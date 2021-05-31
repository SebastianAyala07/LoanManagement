from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from resources.user import UserRegister

from security import authenticate, identity

from db import db
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQL_DATABASE_URI']
app.config['SQLALCHEMY_TECK_MODIFICATIONS'] = False
app.secret_key = os.environ['SECRET_API_KEY']
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity)

api.add_resource(UserRegister, '/api/user/register')


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)