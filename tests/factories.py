import factory

# from product.models import (Category, Brand, Product,
#                             ProductLine, ProductImage,
#                             ProductType, Attribute,
#                             AttributeValue)

from product.models import Category, Product, ProductLine, ProductImage, ProductType


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: 'test_category_%d' % n)
    slug = factory.Sequence(lambda n: 'test_slug_%d' % n)


#
#
# class AttributeFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Attribute
#
#     name = 'attribute_name_test'
#     description = 'attr_description_test'


class ProductTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductType

    name = factory.Sequence(lambda n: 'test_type_name_%d' % n)

    # @factory.post_generation
    # def attribute(self, create, extracted, **kwargs):
    #     if not create or not extracted:
    #         return
    #     self.attribute.add(*extracted)


# class AttributeValueFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = AttributeValue
#
#     attr_value = 'attr_test'
#     attribute = factory.SubFactory(AttributeFactory)
#
#
class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: 'test_product_name_%d' % n)
    pid = factory.Sequence(lambda n: '0000_%d' % n)
    description = 'test_description'
    is_digital = True
    category = factory.SubFactory(CategoryFactory)
    is_active = True
    product_type = factory.SubFactory(ProductTypeFactory)


class ProductLineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductLine

    price = 10.00
    sku = '0123456789'
    stock_qty = 1
    product = factory.SubFactory(ProductFactory)
    is_active = True
    weight = 100
    product_type = factory.SubFactory(ProductTypeFactory)


class ProductImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductImage

    alternative_text = 'test alternative text'
    url = 'test.jpg'
    productline = factory.SubFactory(ProductLineFactory)
