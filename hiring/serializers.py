from rest_framework import serializers
from .models import User, ChatMessage
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token
import logging

logger = logging.getLogger(__name__)

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    token = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_admin', 'is_recruiter', 'is_staff', 'is_active', 'token']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def get_token(self, obj):
        token, _ = Token.objects.get_or_create(user=obj)
        return token.key
    
    def validate_password(self, value):
        # Validate password
        validate_password(value)
        return value
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.is_active = True
        if user.is_admin:
            user.is_staff = True
            user.is_superuser = True
        user.save()
        Token.objects.create(user=user)
        return user
    
    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        # Update staff and superuser status based on admin status
        if 'is_admin' in validated_data:
            instance.is_staff = validated_data['is_admin']
            instance.is_superuser = validated_data['is_admin']
        return super().update(instance, validated_data)

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'message', 'sender', 'timestamp']
        read_only_fields = ['id', 'timestamp']

    def create(self, validated_data):
        logger.info(f"Serializer create called with data: {validated_data}")
        return super().create(validated_data)