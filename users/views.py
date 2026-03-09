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


class FirebaseSyncView(APIView):
    """Webhook/manual endpoint to sync user profile from Firebase.

    Security: Accepts either a valid Firebase ID token in Authorization header
    or a shared secret in header `X-FIREBASE-SYNC-SECRET` set in settings.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        from django.conf import settings
        firebase_service = get_firebase_service()

        # Authentication: either Firebase ID token or shared secret header
        auth_header = request.META.get('HTTP_AUTHORIZATION', '').split()
        secret_header = request.META.get('HTTP_X_FIREBASE_SYNC_SECRET')

        uid = None
        if auth_header and len(auth_header) == 2 and auth_header[0] == 'Bearer':
            token = auth_header[1]
            decoded = firebase_service.verify_token(token)
            if not decoded:
                return Response({'success': False, 'error': 'Invalid Firebase token'}, status=status.HTTP_401_UNAUTHORIZED)
            uid = decoded.get('uid')
        elif not secret_header or secret_header != getattr(settings, 'FIREBASE_SYNC_SECRET', None):
            return Response({'success': False, 'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        if not uid:
            uid = data.get('uid')
        if not uid:
            return Response({'success': False, 'error': 'uid is required'}, status=status.HTTP_400_BAD_REQUEST)

        action = data.get('action', 'update')

        try:
            user = BaseUser.objects.get(firebase_uid=uid)
        except BaseUser.DoesNotExist:
            user = None

        if action == 'delete':
            if user:
                user.is_active = False
                user.synced_at = timezone.now()
                user.save()
                return Response({'success': True, 'status': 'deleted'}, status=status.HTTP_200_OK)
            else:
                return Response({'success': False, 'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Update/create from Firebase record
        fb_user = firebase_service.get_user(uid)
        if not fb_user:
            return Response({'success': False, 'error': 'Firebase user not found'}, status=status.HTTP_404_NOT_FOUND)

        if user is None:
            user = BaseUser.objects.create(
                firebase_uid=uid,
                email=fb_user.get('email') or '',
                name=fb_user.get('display_name') or '',
                firebase_profile=fb_user,
                auth_provider='firebase',
                is_active=True,
                synced_at=timezone.now()
            )
        else:
            user.email = fb_user.get('email') or user.email
            user.name = fb_user.get('display_name') or user.name
            user.firebase_profile = fb_user
            user.auth_provider = 'firebase'
            user.is_active = True
            user.synced_at = timezone.now()
            user.save()

        serializer = BaseUserSerializer(user)
        return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
