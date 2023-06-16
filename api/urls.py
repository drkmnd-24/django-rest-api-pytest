from django.urls import path, include

from product.api.views import CategoryView, BrandView, ProductView

from rest_framework.routers import DefaultRouter

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

router = DefaultRouter()

router.register(r'category', CategoryView)
router.register(r'brand', BrandView)
router.register(r'product', ProductView)

urlpatterns = [
    path('', include(router.urls)),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema')),
]
