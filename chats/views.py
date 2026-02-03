"""Views for chat functionality."""

import logging
from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import ChatRoom, Message
from .serializers import (
    ChatRoomListSerializer,
    ChatRoomDetailSerializer,
    MessageSerializer,
    MessageCreateSerializer,
    VoiceMessageUploadSerializer,
)
from users.models import BaseUser

logger = logging.getLogger(__name__)


class ChatRoomViewSet(viewsets.ModelViewSet):
    """ViewSet for managing chat rooms."""
    
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Get chat rooms for the current user."""
        user = self.request.user
        return ChatRoom.objects.filter(
            participant_1=user
        ) | ChatRoom.objects.filter(
            participant_2=user
        )
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'retrieve':
            return ChatRoomDetailSerializer
        return ChatRoomListSerializer
    
    def get_serializer_context(self):
        """Add request to serializer context."""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    @action(detail=False, methods=['post'], url_path='start-chat')
    def start_chat(self, request):
        """Start or get a chat room with another user."""
        other_user_id = request.data.get('other_user_id')
        
        if not other_user_id:
            return Response(
                {'error': 'other_user_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            other_user = BaseUser.objects.get(id=other_user_id)
        except BaseUser.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if request.user.id == other_user.id:
            return Response(
                {'error': 'Cannot start chat with yourself'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get or create chat room
        user1, user2 = sorted([request.user, other_user], key=lambda u: str(u.id))
        room, created = ChatRoom.objects.get_or_create(
            participant_1=user1,
            participant_2=user2,
        )
        
        serializer = ChatRoomDetailSerializer(room, context=self.get_serializer_context())
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail='pk', methods=['post'], url_path='send-message')
    def send_message(self, request, pk=None):
        """Send a text message in the chat room."""
        room = self.get_object()
        serializer = MessageCreateSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        text = serializer.validated_data.get('text', '').strip()
        message_type = serializer.validated_data.get('message_type', 'text')
        attachment_url = serializer.validated_data.get('attachment_url')
        
        if not text and not attachment_url:
            return Response(
                {'error': 'Message cannot be empty'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        message = Message.objects.create(
            room=room,
            sender=request.user,
            text=text,
            message_type=message_type,
            attachment_url=attachment_url,
        )
        
        room.last_message_at = message.timestamp
        room.save(update_fields=['last_message_at'])
        
        return Response(
            MessageSerializer(message, context=self.get_serializer_context()).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail='pk', methods=['post'], url_path='send-voice')
    def send_voice_message(self, request, pk=None):
        """Send a voice message in the chat room."""
        room = self.get_object()
        serializer = VoiceMessageUploadSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        audio_file = serializer.validated_data['audio_file']
        audio_duration = serializer.validated_data['audio_duration']
        
        message = Message.objects.create(
            room=room,
            sender=request.user,
            message_type='audio',
            audio_file=audio_file,
            audio_duration=audio_duration,
        )
        
        room.last_message_at = message.timestamp
        room.save(update_fields=['last_message_at'])
        
        logger.info(f"Voice message created: {message.id} by {request.user.email}")
        
        return Response(
            MessageSerializer(message, context=self.get_serializer_context()).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail='pk', methods=['get'], url_path='messages')
    def get_messages(self, request, pk=None):
        """Get all messages in a chat room with pagination."""
        room = self.get_object()
        messages = room.messages.all()
        
        # Pagination
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 50))
        start = (page - 1) * page_size
        end = start + page_size
        
        serializer = MessageSerializer(
            messages[start:end],
            many=True,
            context=self.get_serializer_context()
        )
        
        return Response({
            'count': messages.count(),
            'page': page,
            'page_size': page_size,
            'results': serializer.data,
        })
