from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'email',
        required=True,
        type=str,
        help="This field cannot be left blank!"
    )
    parser.add_argument(
        'password',
        required=True,
        type=str,
        help="This field cannot be left blank!"
    )

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_email(data['email']):
            return {'message': 'This user already exists'}, 400
        user = UserModel(data['email'], data['password'])
        user.save_to_db()
        return {'message': 'User created successfully'}, 201


class UserList(Resource):

    def get(self):
        return list(
            map(
                lambda x: x.json(), UserModel.query.all()
            )
        )
