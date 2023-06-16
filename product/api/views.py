from product.api.serializers import CategorySerializer, BrandSerializer, ProductSerializer
from product.models import Category, Brand, Product

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema


class CategoryView(viewsets.ViewSet):
    queryset = Category.objects.all()

    @extend_schema(responses=CategorySerializer)
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)