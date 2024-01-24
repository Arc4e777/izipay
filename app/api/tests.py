from django.test import TestCase
from merchants import models
from .models import ServiceAPIKey

import requests
import random, string

# Create your tests here.

transactions_data = [
	{'txid': '3ae19ec9b77380182a31df0fdc8484d519cf6e44ce45bf1775abd216f3a09bd9', 'to_address': 'TAe33rGEByXg26bjfS4ZNJ73H6Qk9sP6hN', 'amount': 4980},
	{'txid': 'b7fb5604a259d3bd9d1da29e9195c9df181ec9c8fbdfbab8a353fca7f04960cc', 'to_address': 'TFzXFncmbVGRAQyM6kVwWZWR6Lrpub9QYx', 'amount': 21.45},
	{'txid': '7f1c856b41c5122e4bee4ff0d8359225b61b7d61c9f4cc4f4df412c2b859da2a', 'to_address': 'TMVNj8RV4TcaH17KZ7ziKLeTeZz5LHtuBQ', 'amount': 0.345},
	{'txid': '5100b8b0c1cb9b0cf2ffe3a1c09a5646cf879274774ac2c5c2454ce6f5113734', 'to_address': 'TG8wXwfqHfhW6jyQjv3q1Fm4iEduYJWJvY', 'amount': 580.11},
	{'txid': '949fafd8b7ce8c31465f0337fa37699ee50a64eb60a0987d53c4805ac516fe6f', 'to_address': 'TYR5CxZu3X7qEYytexfaRjhUBEFdHfzzFF', 'amount': 70.7},
]

incorrect_transactions_data = [
	{'txid': '25eb783a083dd26b19d53aa3448ee665ed9f41715b7e1edd3723af2afa98e0c0', 'to_address': 'TK8Ei4CrpTChR6Zn7SSTS2x14RjcbDuZjq', 'amount': 72108.77},
]

class ApiTestCase(TestCase):
	@classmethod
	def setUpTestData(cls):
		cls.cofix = models.Service.objects.create(name='Cofix')
		cls.cofix_john = models.Trader.objects.create(service=cls.cofix, name='John')

	def test_common(self):
		self.assertEqual(ApiTestCase.cofix.name, 'Cofix')

	def test_right_request(self):
		transaction = random.choice(transactions_data)
		address = models.Address.objects.create(trader=ApiTestCase.cofix_john, address=transaction['to_address'])

		api_key, key = ServiceAPIKey.objects.create_key(name='Base-key', service=ApiTestCase.cofix)
		headers = {'Authorization': f'Api-Key {key}'}
		data = {
			'name': ApiTestCase.cofix_john.name,
			'amount': transaction['amount'],
			'txid': transaction['txid']
		}
		response = self.client.post('/api/validate_bill/', headers=headers, data=data)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json(), {'success': True})

	def test_incorrect_amount_request(self):
		transaction = random.choice(transactions_data)
		address = models.Address.objects.create(trader=ApiTestCase.cofix_john, address=transaction['to_address'])

		api_key, key = ServiceAPIKey.objects.create_key(name='Base-key', service=ApiTestCase.cofix)
		headers = {'Authorization': f'Api-Key {key}'}
		data = {
			'name': ApiTestCase.cofix_john.name,
			'amount': transaction['amount'] - 1,
			'txid': transaction['txid']
		}
		response = self.client.post('/api/validate_bill/', headers=headers, data=data)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json(), {'success': False, 'errors': {'amount': 'Amounts do not match'}})

	def test_incorrect_address_request(self):
		transaction = random.choice(transactions_data)

		api_key, key = ServiceAPIKey.objects.create_key(name='Base-key', service=ApiTestCase.cofix)
		headers = {'Authorization': f'Api-Key {key}'}
		data = {
			'name': ApiTestCase.cofix_john.name,
			'amount': transaction['amount'],
			'txid': transaction['txid']
		}
		response = self.client.post('/api/validate_bill/', headers=headers, data=data)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json(), {'success': False, 'errors': {'txid': 'Address does not belong to the trader'}})

	def test_incorrect_name_request(self):
		transaction = random.choice(transactions_data)

		api_key, key = ServiceAPIKey.objects.create_key(name='Base-key', service=ApiTestCase.cofix)
		headers = {'Authorization': f'Api-Key {key}'}
		data = {
			'name': 'Bob',
			'amount': transaction['amount'],
			'txid': transaction['txid']
		}
		response = self.client.post('/api/validate_bill/', headers=headers, data=data)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json(), {'success': False, 'errors': {'name': 'Trader does not exist'}})

	def test_different_trader_request(self):
		starbucks = models.Service.objects.create(name='Starbucks')
		starbucks_bob = models.Trader.objects.create(service=starbucks, name='Bob')

		transaction = random.choice(transactions_data)
		address = models.Address.objects.create(trader=starbucks_bob, address=transaction['to_address'])

		api_key, key = ServiceAPIKey.objects.create_key(name='Base-key', service=starbucks)
		headers = {'Authorization': f'Api-Key {key}'}
		data = {
			'name': ApiTestCase.cofix_john.name,
			'amount': transaction['amount'],
			'txid': transaction['txid']
		}
		response = self.client.post('/api/validate_bill/', headers=headers, data=data)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.json(), {'success': False, 'errors': {'name': 'Trader does not exist'}})

	def test_incorrect_contract_request(self):
		transaction = incorrect_transactions_data[0]
		address = models.Address.objects.create(trader=ApiTestCase.cofix_john, address=transaction['to_address'])

		api_key, key = ServiceAPIKey.objects.create_key(name='Base-key', service=ApiTestCase.cofix)
		headers = {'Authorization': f'Api-Key {key}'}
		data = {
			'name': ApiTestCase.cofix_john.name,
			'amount': transaction['amount'],
			'txid': transaction['txid']
		}
		response = self.client.post('/api/validate_bill/', headers=headers, data=data)
		self.assertEqual(response.status_code, 400)






