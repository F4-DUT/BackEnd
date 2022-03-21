from rest_framework import routers

from api_account.views import AccountViewSet

app_name = 'api_product'
router = routers.SimpleRouter(trailing_slash=True)

router.register(r'', AccountViewSet, basename='product')

urlpatterns = router.urls
