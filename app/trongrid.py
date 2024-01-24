import os
import requests, json
import base58
from tronpy.abi import trx_abi

from django.core.cache import cache

class TronGrid:
	def __init__(self) -> None:
		self.api_key = os.environ['TRONGRID_APIKEY']
		self.base_url = 'https://api.trongrid.io'

	def hex_to_base58(self, hex_string):
		if hex_string[:2] in ['0x', '0X']:
			hex_string = "41" + hex_string[2:]

		bytes_str = bytes.fromhex(hex_string)
		base58_str = base58.b58encode_check(bytes_str)
		return base58_str.decode('UTF-8')

	def get_transaction(self, txid: str) -> dict:
		response = cache.get(txid)
		if not response:
			url = self.base_url + '/wallet/gettransactionbyid'
			params = {'value': txid}
			headers = {
				'Content-Type': 'application/json',
				'accept': 'application/json',
				'TRON-PRO-API-KEY': self.api_key
			}
			response = requests.post(url, headers=headers, data=json.dumps(params)).json()
			cache.set(txid, response, 600)

		if response == {} or 'Error' in response:
			raise Exception('Invalid hash')

		contract = response['raw_data']['contract'][0]
		contract_type = contract['type']

		match contract_type:
			case 'TransferContract':
				result = {
					'amount': contract['parameter']['value']['amount'] / 1000000,
					'owner_address': self.hex_to_base58(contract['parameter']['value']['owner_address']),
					'to_address': self.hex_to_base58(contract['parameter']['value']['to_address'])
				}

			case 'TriggerSmartContract':
				hex_string = contract['parameter']['value']['data'][4*2:]
				bytes_string = bytes.fromhex(hex_string)
				to_address, amount = trx_abi.decode_abi(['address', 'uint256'], bytes_string)
				result = {
					'amount': amount / 1000000,
					'owner_address': self.hex_to_base58(contract['parameter']['value']['owner_address']),
					'to_address': to_address
				}

			case _:
				raise Exception('Incorrect contract type. Available types: TransferContract, TriggerSmartContract')

		return result




