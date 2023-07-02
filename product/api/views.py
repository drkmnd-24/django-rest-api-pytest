from django.db.models import Prefetch

from api.serializers import CategorySerializer, ProductSerializer, ProductCategorySerializer
from product.models import Category, Product, ProductLine, ProductImage

from rest_framework import viewsets
from rest_framework import status

from rest_framework.response import Response
from rest_framework.decorators import action

from drf_spectacular.utils import extend_schema


class CategoryView(viewsets.ViewSet):
    queryset = Category.objects.all().is_active()

    @extend_schema(responses=CategorySerializer)
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductView(viewsets.ViewSet):
    queryset = Product.objects.all().is_active()
    lookup_field = 'slug'

    def retrieve(self, request, slug=None):
        serializer = ProductSerializer(
            self.queryset.filter(slug=slug)
            .prefetch_related(Prefetch('attribute_value__attribute'))
            .prefetch_related(Prefetch('product_line__product_image'))
            .prefetch_related(Prefetch('product_line__attribute_value__attribute')),
            many=True
        )
        data = Response(serializer.data, status=status.HTTP_200_OK)
        return data

    @action(methods=['get'], detail=False, url_path=r'category/(?P<slug>[\w-]+)')
    def list_product_by_category_slug(self, request, slug=None):
        """
        endpoint to return products by category
        """
        serializer = ProductCategorySerializer(
            self.queryset.filter(category__slug=slug)
            .prefetch_related(
                Prefetch('product_line', queryset=ProductLine.objects.order_by('order'))
            )
            .prefetch_related(
                Prefetch('product_line__product_image', queryset=ProductImage.objects.filter(order=1))
            ), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
