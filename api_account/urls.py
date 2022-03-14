from rest_framework import routers

from api_account.views import AccountViewSet

app_name = 'api_account'
router = routers.SimpleRouter(trailing_slash=True)

router.register(r'account', AccountViewSet, basename='account')

urlpatterns = router.urls
