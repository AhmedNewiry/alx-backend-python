from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessageViewSet, MessageHistoryViewSet, delete_user

router = DefaultRouter()
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'history', MessageHistoryViewSet, basename='message-history')

urlpatterns = [
    path('', include(router.urls)),
    path('user/', delete_user, name='delete_user'),
]