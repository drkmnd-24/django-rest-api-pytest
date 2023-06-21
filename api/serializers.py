from rest_framework import serializers

from product.models import Category, Brand, Product, ProductLine, ProductImage, Attribute, AttributeValue


class CategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='name')

    class Meta:
        model = Category
        fields = ['category_name']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        exclude = ['id']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        exclude = ['id']


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ['name']


class AttributeValueSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer(many=False)

    class Meta:
        model = AttributeValue
        fields = ['attribute', 'attr_value']


class ProductLineSerializer(serializers.ModelSerializer):
    product_image = ProductImageSerializer(many=True)
    attribute_value = AttributeValueSerializer(many=True)

    class Meta:
        model = ProductLine
        fields = [
            'price', 'sku', 'stock_qty',
            'order', 'product_image', 'attribute_value']


class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    category = CategorySerializer()
    product_line = ProductLineSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'
