from initial_data import INITIAL_STATES


class ResponseLoan():

    @classmethod
    def calculate_reponse_by_amount(cls, amount):
        response_json = None
        is_loan = False
        if amount > 50000:
            response_json = INITIAL_STATES.get('denied')
        elif amount == 50000:
            response_json = INITIAL_STATES.get('undecided')
        else:
            response_json = INITIAL_STATES.get('approved')
            is_loan = True
        return response_json.get('code'), is_loan
