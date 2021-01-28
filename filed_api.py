from flask import Blueprint, request, abort, jsonify, Flask
import json
import re
import datetime
from decimal import Decimal
app = Flask(__name__)
@app.route('/')
def index():
	return '<h1>Filed Payment api is running....</h1>'

@app.route("/ProcessPayment", methods=['POST'])
def payment():
	if request.method == 'POST':
		data = request.get_data(as_text=True)
		print(data)
		if not data:
			abort(400)
		request_data = json.loads(data)
		card_data = Card()
		print("request data {}".format(request_data))
		try:
			if not card_data.verify_input(**request_data):
				print("card data invalid")
				abort(400)
		except:
			abort(400)
		try:
			print("Payment status started.....")
			payment_status = ExternalPayment(card_data.Amount, card_data)
			print("Payment process started.....")
			payment_sccessfull = payment_status.make_payment()
			if payment_sccessfull:
				return {"status code": 200}, 200
			else:
				abort(400)
		except:
			abort(500)
	else:
		abort(400)

class BasePaymentGateway:
	def __init__(self, repeat=0):
		self.repeat = repeat
		self.gateway = None
		
	def __repr__(self):
		return "<{}>".format("BasePaymentGateway")
	
	def connect(self, gateway=None, details=None):
		if gateway != None:
			if self.authenticate(details):
				return True
		return False
	
	def authenticate(self, details=None):
		if details != None:
			return True
		return False
	
	def pay(self, amount, user_details=None, gateway=None):
		if gateway is None:
			gateway = self.gateway
		while self.repeat + 1 > 0:
			if self.connect(gateway, user_details):
				print("payment of {} in gateway {} sucessful".format(amount, self.gateway))
				return True
			self.repeat -= 1
		return False


class PremiumBasePaymentGateway(BasePaymentGateway):
	def __init__(self, repeat=3):
		super(PremiumBasePaymentGateway, self).__init__(repeat)
		self.gateway = "PremiumBasePaymentGatway"
	
	def __repr__(self):
		return "<PremiumBasePaymentGateway>"


class ExpensiveBasePaymentGateway(BasePaymentGateway):
	def __init__(self, repeat=1):
		super(ExpensiveBasePaymentGateway, self).__init__(repeat)
		self.gateway = "ExpensiveBasePaymentGateway"
	
	def __repr__(self):
		return "<ExpensiveBasePaymentGateway>"


class CheapBasePaymentGateway(BasePaymentGateway):
	def __init__(self, repeat=0):
		super(CheapBasePaymentGateway, self).__init__(repeat)
		self.gateway = "CheapBasePaymentGateway"
	
	def __repr__(self):
		return "<CheapBasePaymentGateway>"


class ExternalPayment:
	def __init__(self, amount, card_details=None):
		self.amount = amount
		self.card_details = card_details
	
	def make_payment(self):
		try:
			payment_mode = None
			if self.amount <= 20:
				payment_mode = CheapBasePaymentGateway()
			elif 20 < self.amount < 500:
				payment_mode = ExpensiveBasePaymentGateway()
			elif self.amount >= 500:
				payment_mode = PremiumBasePaymentGateway()
			else:
				return False
			
			status = payment_mode.pay(self.amount, self.card_details)
			return status
		except:
			return False
def validate_card(card):
	if not re.search(r"^[456]\d{3}(-?\d{4}){3}$", card) or re.search(r"(\d)\1{3}", re.sub("-", "", card)):
		return False
	return True


class BaseCardDetails:
	def __init__(self):
		self.CreditCardNumber = None
		self.CardHolder = None
		self.ExpirationDate = None
		self.SecurityCode = None
		self.Amount = None


class Card(BaseCardDetails):
	def __init__(self):
		super(Card, self).__init__()
	
	def verify_input(self, **kwargs):
		cards_value = ["CreditCardNumber", "CardHolder", "ExpirationDate", "Amount"]
		if set(cards_value).intersection(kwargs.keys()) != set(cards_value):
			print("card details not found")
			return False
		
		if not type(kwargs['CreditCardNumber'] == str and validate_card(kwargs['CreditCardNumber'])) or not len(kwargs['CreditCardNumber']) == 16:
			print("invalid credit card number")
			return False
		
		if not type(kwargs['CardHolder']) == str:
			print("card holder is not of string type")
			return False
		
		if kwargs.get('SecurityCode',None) :
			if not (type(kwargs.get('SecurityCode', None)) == str and len(kwargs.get('SecurityCode', None)) == 3) or not kwargs.get('SecurityCode', None).isdigit():
				print("security code error")
				return False

		if not datetime.datetime.strptime(kwargs['ExpirationDate'], "%Y/%m/%d") > datetime.datetime.now():
			print("date time error")
			return False
		
		try:
			if not Decimal(kwargs['Amount']) > 0:
				print("amount is invalid")
				return False
		except:
			return False
		
		_data_to_map = {
			"CreditCardNumber": kwargs['CreditCardNumber'],
			'Amount': kwargs['Amount'],
			'CardHolder': kwargs['CardHolder'],

			'ExpirationDate': kwargs['ExpirationDate']
		}
		if kwargs.get("SecurityCode", None):
			_data_to_map.update({"SecurityCode":kwargs.get("SecurityCode")})
		print("input is verified.")
		self.__map_to_card(**kwargs)
		return True
	
	def __map_to_card(self, **kwargs):
		self.CreditCardNumber = kwargs.get('CreditCardNumber', None)
		self.Amount = kwargs.get('Amount', None)
		self.CardHolder = kwargs.get('CardHolder', None)

		self.SecurityCode = kwargs.get('SecurityCode', None)
		self.ExpirationDate = kwargs.get('ExpirationDate', None)
		
		print("Mapping of user input is done sucessfully.")
		return True
	


