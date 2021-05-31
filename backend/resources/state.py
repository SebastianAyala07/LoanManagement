from flask_restful import Resource, reqparse, inputs
from models.state import StateModel


class State(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'code',
        required=True,
        type=str,
        help="This field cannot be left blank!"
    )
    parser.add_argument(
        'description',
        required=True,
        type=str,
        help="This field cannot be left blank!"
    )
    parser.add_argument(
        'apply_for_loan',
        required=True,
        type=inputs.boolean,
        help="This field cannot be left blank!"
    )

    def get(self):
        parser_get = reqparse.RequestParser()
        parser_get.add_argument(
            'code',
            required=True,
            type=str,
            help="This field cannot be left blank!"
        )
        data = parser_get.parse_args()
        state = StateModel.find_by_code(data['code'])
        if state:
            return state.json()
        return {'message': 'State not found'}, 404

    def post(self):
        data = State.parser.parse_args()
        if StateModel.find_by_code(data['code']):
            return {'message': 'A state with that code already exists'}
        state = StateModel(
            data['code'],
            data['description'],
            data['apply_for_loan']
        )
        state.save_to_db()
        return state.json(), 201

    def put(self):
        parser_put = self.parser
        parser_put.add_argument(
            'id',
            required=True,
            type=int,
            help="This field cannot be left blank!"
        )
        data = parser_put.parse_args()
        state = StateModel.find_by_stateid(data['id'])
        if state is None:
            state = StateModel(
                data['code'], data['description'], data['apply_for_loan']
            )
        else:
            state.code = data['code']
            state.description = data['description']
            state.apply_for_loan = data['apply_for_loan']
        state.save_to_db()
        return state.json()

    def delete(self):
        parser_delete = reqparse.RequestParser()
        parser_delete.add_argument(
            'id',
            required=True,
            type=int,
            help="This field cannot be left blank!"
        )
        data = parser_delete.parse_args()
        state = StateModel.find_by_stateid(data['id'])
        state.delete_from_db()
        return {'message': 'State deleted'}


class StateList(Resource):

    def get(self):
        return {
            'states': list(
                map(
                    lambda x: x.json(), StateModel.query.all()
                )
            )
        }
