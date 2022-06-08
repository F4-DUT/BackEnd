from rest_framework import routers
from django.urls import path


from websocket.views import MessageSendAPIView

app_name = 'websocket'
router = routers.SimpleRouter(trailing_slash=True)

urlpatterns = [
    path('', MessageSendAPIView.info),
]