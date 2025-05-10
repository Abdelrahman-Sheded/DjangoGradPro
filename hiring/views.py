from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import  User, ChatHistory
from .serializers import  UserSerializer, ChatHistorySerializer
from django.http import HttpResponse, JsonResponse
import httpx
from .permissions import IsAdminUser



def home(request):
    return HttpResponse("Welcome to Hiring App!")

async def rag_query(request):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8001/generate",
            json={"text": "Hello RAG!"}
        )
    return JsonResponse(response.json())

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        return [IsAuthenticated()]

class ChatHistoryViewSet(viewsets.ModelViewSet):
    queryset = ChatHistory.objects.all()
    serializer_class = ChatHistorySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return ChatHistory.objects.filter(user=self.request.user)