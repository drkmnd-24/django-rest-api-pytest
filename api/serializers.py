from rest_framework import serializers

from product.models import (Category, Product, ProductLine,
                            ProductImage, Attribute, AttributeValue)


class CategorySerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='name')

    class Meta:
        model = Category
        fields = ['category', 'slug']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        exclude = ['id', 'productline']


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ['id', 'name']


class AttributeValueSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer(many=False)

    class Meta:
        model = AttributeValue
        fields = ['attribute', 'attr_value']


class ProductLineSerializer(serializers.ModelSerializer):
    attribute_value = AttributeValueSerializer(many=True)
    product_image = ProductImageSerializer(many=True)

    class Meta:
        model = ProductLine
        fields = [
            'price', 'sku', 'stock_qty',
            'order', 'product_image',
            'attribute_value'
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        av_data = data.pop('attribute_value')
        attrib_values = {}
        for key in av_data:
            attrib_values.update({key['attribute']['name']: key['attr_value']})
        data.update({'specification': attrib_values})
        return data


class ProductLineCategorySerializer(serializers.ModelSerializer):
    product_image = ProductImageSerializer(many=True)

    class Meta:
        model = ProductLine
        fields = ['price', 'product_image']


class ProductCategorySerializer(serializers.ModelSerializer):
    product_line = ProductLineCategorySerializer(many=True)

    class Meta:
        model = Product
        fields = ["name", "slug", "pid", "created_at", "product_line"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        x = data.pop("product_line")

        if x:
            price = x[0]["price"]
            image = x[0]["product_image"]
            data.update({"price": price})
            data.update({"image": image})

        return data


class ProductSerializer(serializers.ModelSerializer):
    product_line = ProductLineSerializer(many=True)
    attribute_value = AttributeValueSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            'name', 'slug', 'pid', 'description',
            'product_line', 'attribute_value'
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        av_data = data.pop("attribute_value")
        attr_values = {}
        for key in av_data:
            attr_values.update({key["attribute"]['name']: key["attr_value"]})
        data.update({"attribute": attr_values})

        return data
