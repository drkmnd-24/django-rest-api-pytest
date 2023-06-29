from rest_framework import serializers

from product.models import Category, Product, ProductLine, ProductImage, Attribute, AttributeValue


class CategorySerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='name')

    class Meta:
        model = Category
        fields = ['category', 'slug']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        exclude = ['id']


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

    class Meta:
        model = ProductLine
        fields = [
            'price', 'sku', 'stock_qty',
            'order', 'product_image', 'attribute_value']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        av_data = data.pop('attribute_value')
        attrib_values = {}
        for key in av_data:
            attrib_values.update({key['attribute']['id']: key['attr_value']})
        data.update({'specification': attrib_values})
        return data


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name')
    product_line = ProductLineSerializer(many=True)
    attribute = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'name', 'slug', 'description',
            'category_name', 'product_line',
            'attribute']

    def get_attribute(self, obj):
        attribute = Attribute.objects.filter(product_type_attr__product__id=obj.id)
        return AttributeSerializer(attribute, many=True).data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        av_data = data.pop("attribute")
        attr_values = {}
        for key in av_data:
            attr_values.update({key["id"]: key["name"]})
        data.update({"type specification": attr_values})

        return data
