import pytest
import requests
import json

url = "http://{}:{}".format("127.0.0.1", "5000")

def test_check_security_code():
    # check SecurityCode cases
    card_data_1 = {"CreditCardNumber": "3232312312312321", "CardHolder": "Mohit Verma", "SecurityCode": "123",
                   "ExpirationDate": "2022/06/04", "Amount": 333.3}
    card_data_2 = {"CreditCardNumber": "4343423423424234", "CardHolder": "Mohit Verma", "ExpirationDate": "2022/07/07", "Amount": 333.3}
    card_data_3 = {"CreditCardNumber": "2323232323232323", "CardHolder": "Mohit Verma", "SecurityCode": 111,
                   "ExpirationDate": "2022/02/05", "Amount": 333.3}

    response_1 = requests.post("{}/ProcessPayment".format(url), data=json.dumps(card_data_1),
                               headers={"Content-Type": "application/json"})
    
    response_2 = requests.post("{}/ProcessPayment".format(url), data=json.dumps(card_data_2),
                               headers={"Content-Type": "application/json"})
    response_3 = requests.post("{}/ProcessPayment".format(url), data=json.dumps(card_data_3),
                               headers={"Content-Type": "application/json"})
    assert response_1.status_code == 200
    assert response_2.status_code == 200
    assert response_3.status_code == 400

def test_check_no_data():
    # Check for request body has no data
    card_data = {}
    response = requests.post("{}/ProcessPayment".format(url), data=json.dumps(card_data),
                             headers={"Content-Type": "application/json"})
    assert response.status_code == 400


def test_check_invalid_argument():
    # Check request body has invalid argument, as compared to argument which is required
    card_data = dict(CreditCardNumbers="1234567890094949", CardHoldewr="Mohit Verma", SecurityCode="123", ExpirationDate="2020/03/03", Amount=1000)
    response = requests.post("{}/ProcessPayment".format(url), data=json.dumps(card_data), headers={"Content-Type": "application/json"})
    assert response.status_code == 400

def test_check_invalid_request_type():
    #Check api behaviour for different request type
    response = requests.get("{}/ProcessPayment".format(url))
    
    assert response.status_code >= 400


def test_check_ext_invalid_credit_card_info():
    # Check for various cases when CreditCardNumber value is different, checking validity of credit
    card_data_1 = {"CreditCardNumber": "qwer123456ijiojw","CardHolder":"Mohit Verma","SecurityCode": "123",
"ExpirationDate": "2020/05/05","Amount": 1000}
    card_data_2 = {"CreditCardNumber": "1234567890123456", "CardHolder": "Mohit Verma", "SecurityCode": "123",
                   "ExpirationDate": "2022/11/12", "Amount": 2000}
    response_1 = requests.post("{}/ProcessPayment".format(url), data=json.dumps(card_data_1), headers={"Content-Type":"application/json"})
    response_2 = requests.post("{}/ProcessPayment".format(url), data=json.dumps(card_data_2), headers={"Content-Type": "application/json"})
    
    assert response_1.status_code == 400
    assert response_2.status_code == 200
    
    
def test_check_input_data_for_various_amount():
    # Check for different amount input different external payment method 
    card_data_1 = {"CreditCardNumber": "1234567890123456", "CardHolder": "Mohit Verma", "SecurityCode": "123",
                   "ExpirationDate": "2022/11/12", "Amount": 18}
    card_data_2 = {"CreditCardNumber": "1234567890123456", "CardHolder": "Mohit Verma", "SecurityCode": "111",
                   "ExpirationDate": "2022/11/12", "Amount": 332}
    card_data_3 = {"CreditCardNumber": "1234567890123456", "CardHolder": "Mohit Verma", "SecurityCode": "111",
                   "ExpirationDate": "2022/11/12", "Amount": 668}
    
    response_1 = requests.post("{}/ProcessPayment".format(url), data=json.dumps(card_data_1), headers={"Content-Type":"application/json"})
    response_2 = requests.post("{}/ProcessPayment".format(url), data=json.dumps(card_data_2), headers={"Content-Type":"application/json"})
    response_3 = requests.post("{}/ProcessPayment".format(url), data=json.dumps(card_data_3), headers={"Content-Type":"application/json"})
    
    assert response_1.status_code == 200
    assert response_2.status_code == 200
    assert response_3.status_code == 200


def test_check_payment_ext_exp_date():
    # check ExpirationDate different case, when date is more then present and when date is past of present date
    card_data_1 = {"CreditCardNumber": "4343423423424234", "CardHolder": "Mohit Verma", "SecurityCode": "123",
                   "ExpirationDate": "2022/01/11", "Amount": 1000}
    card_data_2 = {"CreditCardNumber": "1234567890123456", "CardHolder": "Mohit Verma", "SecurityCode": "123",
                   "ExpirationDate": "2019/11/12", "Amount": 2000}
    
    response_1 = requests.post("{}/ProcessPayment".format(url), data=json.dumps(card_data_1), headers={"Content-Type": "application/json"})
    response_2 = requests.post("{}/ProcessPayment".format(url), data=json.dumps(card_data_2),
                               headers={"Content-Type": "application/json"})
    
    assert response_1.status_code == 200
    assert response_2.status_code == 400


