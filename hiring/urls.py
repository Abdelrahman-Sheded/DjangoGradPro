from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ChatMessageViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'messages', ChatMessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
]