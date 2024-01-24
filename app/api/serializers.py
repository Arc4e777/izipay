from rest_framework import serializers


class BillSerializer(serializers.Serializer):
	name = serializers.CharField(max_length=100)
	amount = serializers.FloatField()
	txid = serializers.CharField(max_length=200)