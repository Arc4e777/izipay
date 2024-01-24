from rest_framework.response import Response
from rest_framework import status

from rest_framework.views import APIView

from .permissions import HasServiceAPIKey
from .serializers import BillSerializer
from .models import ServiceAPIKey

from merchants import models

from trongrid import TronGrid

import logging
import json
# Create your views here.

logger = logging.getLogger('api')

class ValidateBillView(APIView):
	permission_classes = [HasServiceAPIKey]

	def post(self, request) -> Response:
		log_data = {'method': request.method, 'url': request.get_full_path()}

		bill = BillSerializer(data=request.data)
		if bill.is_valid():
			key = request.META["HTTP_AUTHORIZATION"].split()[1]
			api_key = ServiceAPIKey.objects.get_from_key(key)
			service = api_key.service

			qs = models.Trader.objects.filter(service=service, name=bill.data['name'])
			if not qs.exists():
				response = {'success': False, 'errors': {'name': 'Trader does not exist'}}
				log_data['response'] = response
				logger.error(log_data)

				return Response(response, status=status.HTTP_400_BAD_REQUEST)
			
			trongrid = TronGrid()
			try:
				transaction = trongrid.get_transaction(bill.data['txid'])
			except Exception as e:
				response = {'success': False, 'errors': {'txid': str(e)}}
				log_data['response'] = response
				logger.error(log_data)

				return Response(response, status=status.HTTP_400_BAD_REQUEST)

			trader = qs.first()
			if bill.data['amount'] != transaction['amount']:
				response = {'success': False, 'errors': {'amount': 'Amounts do not match'}}
				log_data['response'] = response
				logger.error(log_data)

				return Response(response, status=status.HTTP_400_BAD_REQUEST)

			if transaction['to_address'] not in trader.get_address_list():
				response = {'success': False, 'errors': {'txid': 'Address does not belong to the trader'}}
				log_data['response'] = response
				logger.error(log_data)

				return Response(response, status=status.HTTP_400_BAD_REQUEST)

			response = {'success': True}
			log_data['response'] = response
			logger.info(log_data)

			return Response(response, status=status.HTTP_200_OK)

		response = {'success': False, 'errors': bill.errors}
		log_data['response'] = response
		logger.error(log_data)

		return Response(response, status=status.HTTP_400_BAD_REQUEST)
		








