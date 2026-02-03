"""Views for users app."""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from .models import BaseUser, UserAvatar, DeviceToken
from .serializers import (
    BaseUserSerializer, UserUpdateSerializer, UserVerifySerializer,
    UserProfileSerializer, DeviceTokenSerializer, DeviceTokenCreateSerializer
)


class AuthVerifyView(APIView):
    """Verify Firebase token and return user data."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        serializer = UserVerifySerializer(user)
        return Response({
            'success': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class UserProfileDetailView(APIView):
    """Get authenticated user's profile."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = BaseUserSerializer(request.user)
        return Response({
            'success': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class UserProfileUpdateView(APIView):
    """Update authenticated user's profile."""
    permission_classes = [IsAuthenticated]
    
    def put(self, request):
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            'success': True,
            'data': BaseUserSerializer(request.user).data
        }, status=status.HTTP_200_OK)


class UserPublicProfileView(APIView):
    """Get public profile of a user."""
    permission_classes = [AllowAny]
    
    def get(self, request, user_id):
        try:
            user = BaseUser.objects.get(id=user_id)
        except BaseUser.DoesNotExist:
            return Response({
                'success': False,
                'error': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserProfileSerializer(user)
        return Response({
            'success': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class AvatarUploadView(APIView):
    """Upload user avatar."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({
                'success': False,
                'error': 'No file provided'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # In production, upload to S3 or cloud storage
        avatar, _ = UserAvatar.objects.get_or_create(user=request.user)
        avatar.url = f"/media/avatars/{request.user.id}.jpg"
        avatar.save()
        
        return Response({
            'success': True,
            'data': {
                'url': avatar.url,
                'uploadedAt': avatar.uploaded_at.isoformat()
            }
        }, status=status.HTTP_201_CREATED)


class DeviceTokenRegisterView(APIView):
    """Register device token for push notifications."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = DeviceTokenCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        device_token, _ = DeviceToken.objects.get_or_create(
            user=request.user,
            token=serializer.validated_data['token'],
            defaults={'platform': serializer.validated_data['platform']}
        )
        
        return Response({
            'success': True,
            'data': DeviceTokenSerializer(device_token).data
        }, status=status.HTTP_201_CREATED)
