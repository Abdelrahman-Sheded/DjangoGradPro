from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User, ChatMessage
from .serializers import UserSerializer, ChatMessageSerializer
from django.http import HttpResponse
from .permissions import IsAdminUser
import logging

logger = logging.getLogger(__name__)

def home(request):
    return HttpResponse("Welcome to Hiring App!")

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]  
        if self.action in ['destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        return [IsAuthenticated()]

class ChatMessageViewSet(viewsets.ModelViewSet):
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ChatMessage.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        logger.info(f"Creating message: {serializer.validated_data}")
        message = serializer.save(user=self.request.user)
        logger.info(f"Message created: {message.id}")
        return message

    def create(self, request, *args, **kwargs):
        logger.info(f"Received create request: {request.data}")
        return super().create(request, *args, **kwargs)