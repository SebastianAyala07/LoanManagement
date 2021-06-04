from datetime import date
import unittest
import json
import os

from app import app
from db import db


class UserTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.db = db.init_app(app)
        self.user_test = os.environ['USER_TEST']
        self.password_test = os.environ['USER_TEST_PASSWORD']
        auth = self.app.post(
            '/auth',
            headers={
                "Content-Type": "application/json"
            },
            data=json.dumps({
                "username": self.user_test,
                "password": self.password_test
            })
        )
        access_token = auth.get_json()
        self.headers = {
            "Authorization": "JWT {}".format(access_token.get('access_token')),
            "Content-Type": "application/json"
        }

    def test_successful_create_user(self):
        payload = json.dumps(
            {
                "email": "testsebastianayala@sagmail.com",
                "password": "tests23duje4Q@"
            }
        )

        response = self.app.post(
            '/api/user/register',
            headers=self.headers,
            data=payload
        )

        self.assertEqual(201, response.status_code)

    def test_create_user_without_password(self):
        payload = json.dumps(
            {
                "email": "testsebastianayala@sagmail.com",
            }
        )

        response = self.app.post(
            '/api/user/register',
            headers=self.headers,
            data=payload
        )

        self.assertEqual(400, response.status_code)

    def test_create_user_without_email(self):
        payload = json.dumps(
            {
                "password": "tests23duje4Q@",
            }
        )

        response = self.app.post(
            '/api/user/register',
            headers=self.headers,
            data=payload
        )

        self.assertEqual(400, response.status_code)

    def tearDown(self):
        pass


class TestLoan(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.db = db.init_app(app)
        self.user_test = os.environ['USER_TEST']
        self.password_test = os.environ['USER_TEST_PASSWORD']
        auth = self.app.post(
            '/auth',
            headers={
                "Content-Type": "application/json"
            },
            data=json.dumps({
                "username": self.user_test,
                "password": self.password_test
            })
        )
        access_token = auth.get_json()
        self.headers = {
            "Authorization": "JWT {}".format(access_token.get('access_token')),
            "Content-Type": "application/json"
        }

    def test_create_request_loan_approved(self):
        payload = json.dumps(
            {
                "fiscal_number": "1234534",
                "company_name": "SAG S.A.S",
                "amount_money": 48000,
                "number_installments": 60,
            }
        )

        response = self.app.post(
            '/api/loan',
            headers=self.headers,
            data=payload
        )

        self.assertEqual(201, response.status_code)
        # loan_request = response.get_json()
        # self.assertTrue(loan_request.get('is_loan'))
        # self.assertTrue(loan_request.state.description == 'approved')

    def test_create_request_loan_declined(self):
        payload = json.dumps(
            {
                "fiscal_number": "1234534",
                "company_name": "SAG S.A.S",
                "amount_money": 560000,
                "number_installments": 60,
            }
        )

        response = self.app.post(
            '/api/loan',
            headers=self.headers,
            data=payload
        )

        self.assertEqual(201, response.status_code)
        # loan_request = response[0]
        # self.assertTrue(loan_request.is_loan)
        # self.assertTrue(loan_request.state.description == 'declined')

    def test_create_request_loan_undecided(self):
        payload = json.dumps(
            {
                "fiscal_number": "1234534",
                "company_name": "SAG S.A.S",
                "amount_money": 50000,
                "number_installments": 60,
            }
        )

        response = self.app.post(
            '/api/loan',
            headers=self.headers,
            data=payload
        )

        self.assertEqual(201, response.status_code)
        # loan_request = response[0]
        # self.assertTrue(loan_request.is_loan)
        # self.assertTrue(loan_request.state.description == 'undecided')

    def test_create_request_loan_negative_amount(self):
        payload = json.dumps(
            {
                "fiscal_number": "1234534",
                "company_name": "SAG S.A.S",
                "amount_money": -50,
                "number_installments": 60,
            }
        )

        response = self.app.post(
            '/api/loan',
            headers=self.headers,
            data=payload
        )

        self.assertEqual(400, response.status_code)

    def test_create_request_loan_zero_amount(self):
        payload = json.dumps(
            {
                "fiscal_number": "1234534",
                "company_name": "SAG S.A.S",
                "amount_money": 0,
                "number_installments": 60,
            }
        )

        response = self.app.post(
            '/api/loan',
            headers=self.headers,
            data=payload
        )

        self.assertEqual(400, response.status_code)


class TestPayment(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.db = db.init_app(app)
        self.user_test = os.environ['USER_TEST']
        self.password_test = os.environ['USER_TEST_PASSWORD']
        auth = self.app.post(
            '/auth',
            headers={
                "Content-Type": "application/json"
            },
            data=json.dumps({
                "username": self.user_test,
                "password": self.password_test
            })
        )
        access_token = auth.get_json()
        self.headers = {
            "Authorization": "JWT {}".format(access_token.get('access_token')),
            "Content-Type": "application/json"
        }
        self.payload_loan = json.dumps(
            {
                "fiscal_number": "1234534",
                "company_name": "SAG S.A.S",
                "amount_money": 48000,
                "number_installments": 60,
            }
        )
        self.response = self.app.post(
            '/api/loan',
            headers=self.headers,
            data=self.payload_loan
        )
        loan = self.response.get_json()
        loan['accept_terms_conditions'] = True
        self.response = self.app.put(
            '/api/loan',
            headers=self.headers,
            data=json.dumps(loan)
        )
        print(f"\n\nDFR{self.response.get_json()}\n\n")

    def test_generate_payments(self):
        loan_data = self.response.get_json()
        payload = json.dumps(
            {
                "loan_id": loan_data.get('id')
            }
        )

        response = self.app.post(
            '/api/payments/generate',
            headers=self.headers,
            data=payload
        )
        print(f"\n\nER{response.get_json()}\n\n")

        self.assertEqual(201, response.status_code)

    def test_create_payment(self):
        loan_data = self.response.get_json()
        date_today = date.today()
        payload = json.dumps(
            {
                "loan_id": loan_data.get('id'),
                "date_payment_deadline": date_today.isoformat(),
                "date_payment_efective": date_today.isoformat(),
                "is_active": False,
                "amount_pay": 3000
            }
        )

        response = self.app.post(
            '/api/payment',
            headers=self.headers,
            data=payload
        )
        print(f"\n\nTT{response.get_json()}\n\n")

        self.assertEqual(200, response.status_code)
