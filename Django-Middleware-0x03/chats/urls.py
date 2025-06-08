from django.urls import path, include
from rest_framework_nested.routers import NestedDefaultRouter
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet

base_router = DefaultRouter()
base_router.register(r'conversations', ConversationViewSet)
nested_router = NestedDefaultRouter(base_router, r'conversations', lookup='conversation')
nested_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(base_router.urls)),
    path('', include(nested_router.urls)),
]