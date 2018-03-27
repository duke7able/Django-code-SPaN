from rest_framework import serializers
from .models import stock

class StockSerializer(serializers.ModelSerializer):

    class Meta:
        model = stock
        # fields = ('ticker', 'volume')
        # if we wanna return some particular values
        fields = '__all__'
        # fields will contain things that you need to returned by the REST api