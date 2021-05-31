from datetime import datetime, timezone
import unittest
import json
import os

from app import app
from db import db


class UserTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.db = db.get_db()
        self.user_test = os.environ['USER_TEST']
        self.password_test = os.environ['USER_TEST_PASSWORD']
        auth = self.app.post(
            '/auth',
            headers={
                "Content-Type": "application/json"
            },
            data={
                "email": self.user_test,
                "password": self.password_test
            }
        )
        self.headers = {
            "Authorization": "JWT {}".format((auth.json())['access_token']),
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
        self.db = db.get_db()
        self.user_test = os.environ['USER_TEST']
        self.password_test = os.environ['USER_TEST_PASSWORD']
        auth = self.app.post(
            '/auth',
            headers={
                "Content-Type": "application/json"
            },
            data={
                "email": self.user_test,
                "password": self.password_test
            }
        )
        self.headers = {
            "Authorization": "JWT {}".format((auth.json())['access_token']),
            "Content-Type": "application/json"
        }

    def test_create_request_loan_approved(self):
        payload = json.dumps(
            {
                "fiscal_number": "1234534",
                "company_name": "SAG S.A.S",
                "amount_money": 48000,
                "is_loan": False, #It is not yet a loan. It's a loan application
                "number_installments": 60,
            }
        )

        response = self.app.post(
            '/api/loan',
            headers=self.headers,
            data=payload
        )

        self.assertEqual(201, response.status_code)
        loan_request = response[0]
        self.assertTrue(loan_request.is_loan)
        self.assertTrue(loan_request.state.description == 'approved')

    def test_create_request_loan_declined(self):
        payload = json.dumps(
            {
                "fiscal_number": "1234534",
                "company_name": "SAG S.A.S",
                "amount_money": 560000,
                "is_loan": False,
                "number_installments": 60,
            }
        )

        response = self.app.post(
            '/api/loan',
            headers=self.headers,
            data=payload
        )

        self.assertEqual(201, response.status_code)
        loan_request = response[0]
        self.assertTrue(loan_request.is_loan)
        self.assertTrue(loan_request.state.description == 'declined')

    def test_create_request_loan_undecided(self):
        payload = json.dumps(
            {
                "fiscal_number": "1234534",
                "company_name": "SAG S.A.S",
                "amount_money": 50000,
                "is_loan": False,
                "number_installments": 60,
            }
        )

        response = self.app.post(
            '/api/loan',
            headers=self.headers,
            data=payload
        )

        self.assertEqual(201, response.status_code)
        loan_request = response[0]
        self.assertTrue(loan_request.is_loan)
        self.assertTrue(loan_request.state.description == 'undecided')

    def test_create_request_loan_negative_amount(self):
        payload = json.dumps(
            {
                "fiscal_number": "1234534",
                "company_name": "SAG S.A.S",
                "amount_money": -50,
                "is_loan": False,
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
                "is_loan": False,
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
        self.db = db.get_db()
        self.user_test = os.environ['USER_TEST']
        self.password_test = os.environ['USER_TEST_PASSWORD']
        auth = self.app.post(
            '/auth',
            headers={
                "Content-Type": "application/json"
            },
            data={
                "email": self.user_test,
                "password": self.password_test
            }
        )
        self.headers = {
            "Authorization": "JWT {}".format((auth.json())['access_token']),
            "Content-Type": "application/json"
        }
        self.payload_loan = json.dumps(
            {
                "fiscal_number": "1234534",
                "company_name": "SAG S.A.S",
                "amount_money": 48000,
                "is_loan": False,
                "number_installments": 60,
            }
        )
        self.response = self.app.post(
            '/api/loan',
            headers=self.headers,
            data=self.payload_loan
        )

    def test_generate_payments(self):
        loan_data = self.response[0]
        payload = json.dumps(
            {
                "loan_id": loan_data.id
            }
        )

        response = self.app.post(
            '/api/payments/generate',
            headers=self.headers,
            data=payload
        )

        self.assertEqual(201, response.status_code)

    def test_create_payment(self):
        loan_data = self.response[0]
        payload = json.dumps(
            {
                "loan_id": loan_data.id,
                "date_payment_deadline": datetime.now(timezone.utc),
                "date_payment_efective": datetime.now(timezone.utc)
            }
        )

        response = self.app.put(
            '/api/payment',
            headers=self.headers,
            data=payload
        )

        self.assertEqual(200, response.status_code)