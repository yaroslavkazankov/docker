from rest_framework import serializers
from .models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ('product', 'quantity', 'price')


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['address', 'positions']

    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)

        for position in positions:
            StockProduct.objects.update_or_create(stock=stock, **position)
        return stock

    def update(self, instance, validated_data):
        stock = instance
        positions = validated_data.pop('positions')

        stock.positions.all().delete()
        stock.save()

        for position in positions:
            StockProduct.objects.update_or_create(stock=stock, **position)
        return stock
