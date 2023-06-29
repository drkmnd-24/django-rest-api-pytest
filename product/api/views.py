from api.serializers import CategorySerializer, ProductSerializer
from product.models import Category, Product

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
            Product.objects.filter(slug=slug).select_related('category'), many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(responses=ProductSerializer)
    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path=r'category/(?P<slug>[\w-]+)')
    def list_product_by_category_slug(self, request, slug=None):
        """
        endpoint to return products by category
        """
        serializer = ProductSerializer(self.queryset.filter(category__slug=slug), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
