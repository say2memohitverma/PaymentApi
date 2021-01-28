# PaymentApi
How to Run:
1. Open the project folder
2. Run on command prompt: python -m pipenv install
3. Run on command prompt: python -m flask run

How to Test:

A. Test with Postman:

1. Open postman
2. Copy following url in urlbar with post type method :
http://127.0.0.1:5000/ProcessPayment
<img scr=api_screenshot.png/>
3. Copy following header in header's bar :  
Content-Type:application/json
4. Copy following data in body parameter bar : 
{"CreditCardNumber": "1234123412341234", "CardHolder": "Mohit Verma", "ExpirationDate": "2022/01/01", "Amount": 100}
5. Click on send button
6. Got 200 response and also check flask api cmd promot for request processed

B. Test with pytest
1. Open the project folder
2. Open cmd promt and type following command in prompt:
python -m pytest testing_code.py
3. All the test are passed and also check api command prompt for request processed
