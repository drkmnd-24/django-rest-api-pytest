from rest_framework import serializers

from product.models import Category, Brand, Product, ProductLine


class CategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='name')

    class Meta:
        model = Category
        fields = ['category_name']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        exclude = ['id']


class ProductLineSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductLine
        exclude = ['id', 'is_active', 'product']


class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    category = CategorySerializer()
    product_line = ProductLineSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'
