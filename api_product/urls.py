from rest_framework import routers

from api_product.views import CategoryViewSet, ProductViewSet

app_name = 'api_product'
router = routers.SimpleRouter(trailing_slash=True)

router.register(r'category', CategoryViewSet, basename='product')
router.register(r'', ProductViewSet, basename='product')

urlpatterns = router.urls
