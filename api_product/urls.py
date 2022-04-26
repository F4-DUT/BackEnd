from rest_framework import routers

from api_product.views import CategoryViewSet, ProductViewSet
from api_product.views import ProductImageViewSet
from api_product.views.Dataset import DatasetViewSet

app_name = 'api_product'
router = routers.SimpleRouter(trailing_slash=True)

router.register(r'productImage', ProductImageViewSet, basename='productImage')
router.register(r'dataset', DatasetViewSet, basename='dataset')
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'', ProductViewSet, basename='product')

urlpatterns = router.urls
