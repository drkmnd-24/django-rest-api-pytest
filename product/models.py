from django.db import models
from django.core.exceptions import ValidationError
from mptt.models import MPTTModel, TreeForeignKey

from product.api.fields import OrderField


class ActiveQueryset(models.QuerySet):
    def isactive(self):
        return self.filter(is_active=True)


class Category(MPTTModel):
    name = models.CharField(max_length=100, null=True, blank=True, unique=True)
    slug = models.SlugField(max_length=100)
    is_active = models.BooleanField(default=False)
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)

    objects = ActiveQueryset.as_manager()

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True, unique=True)
    is_active = models.BooleanField(default=False)

    objects = ActiveQueryset.as_manager()

    def __str__(self):
        return self.name


class Product(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = TreeForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=100)
    is_digital = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = ActiveQueryset.as_manager()

    def __str__(self):
        return self.name


class ProductLine(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=6)
    sku = models.CharField(max_length=100)
    stock_qty = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_line')
    is_active = models.BooleanField(default=False)
    order = OrderField(blank=True, unique_for_field='product')
    attribute_value = models.ManyToManyField(
        'AttributeValue', through='ProductLineAttributeValue', related_name='product_line_attribute_value')
    objects = ActiveQueryset.as_manager()

    def clean(self):
        qs = ProductLine.objects.filter(product=self.product)

        for obj in qs:
            if self.id != obj.id and self.order == obj.order:
                raise ValidationError('Duplicate value')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductLine, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.sku)


class Attribute(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    attr_value = models.CharField(max_length=100)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='attribute_value')

    def __str__(self):
        return f'{self.attribute.name}-{self.attr_value}'


class ProductLineAttributeValue(models.Model):
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE, related_name='product_attribute_value_av')
    product_line = models.ForeignKey(ProductLine, on_delete=models.CASCADE, related_name='product_attribute_value_pl')

    class Meta:
        unique_together = ('attribute_value', 'product_line')


class ProductImage(models.Model):
    alternative_text = models.CharField(max_length=100)
    url = models.ImageField(upload_to=None, default='test.jpg')
    productline = models.ForeignKey(ProductLine, on_delete=models.CASCADE, related_name='product_image')
    order = OrderField(unique_for_field='productline', blank=True)

    def clean(self):
        qs = ProductImage.objects.filter(productline=self.productline)
        for obj in qs:
            if self.id != obj.id and self.order == obj.order:
                raise ValidationError('Duplicate value')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductImage, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.order)
