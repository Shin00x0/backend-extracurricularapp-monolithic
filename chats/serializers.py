"""Message and ChatRoom serializers."""

from rest_framework import serializers
from .models import ChatRoom, Message
from users.serializers import UserPublicSerializer


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model."""
    sender = UserPublicSerializer(read_only=True)
    audio_file = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        fields = ('id', 'sender', 'text', 'message_type', 'attachment_url', 'audio_file', 'audio_duration', 'is_read', 'timestamp')
        read_only_fields = ('id', 'sender', 'is_read', 'timestamp', 'audio_file')
    
    def get_audio_file(self, obj):
        """Get the audio file URL."""
        if obj.audio_file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.audio_file.url)
            return obj.audio_file.url
        return None


class ChatRoomListSerializer(serializers.ModelSerializer):
    """Serializer for listing chat rooms."""
    participant_1 = UserPublicSerializer(read_only=True)
    participant_2 = UserPublicSerializer(read_only=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatRoom
        fields = ('id', 'participant_1', 'participant_2', 'created_at', 'last_message_at', 'last_message', 'unread_count')
        read_only_fields = ('id', 'created_at', 'last_message_at')
    
    def get_last_message(self, obj):
        """Get the last message in the chat room."""
        last_message = obj.messages.last()
        if last_message:
            return MessageSerializer(last_message).data
        return None
    
    def get_unread_count(self, obj):
        """Get count of unread messages for the current user."""
        request = self.context.get('request')
        if request and request.user:
            return obj.messages.filter(is_read=False).exclude(sender=request.user).count()
        return 0


class ChatRoomDetailSerializer(serializers.ModelSerializer):
    """Serializer for chat room detail with messages."""
    participant_1 = UserPublicSerializer(read_only=True)
    participant_2 = UserPublicSerializer(read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    room_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = ChatRoom
        fields = ('id', 'room_name', 'participant_1', 'participant_2', 'messages', 'created_at', 'last_message_at')
        read_only_fields = ('id', 'created_at', 'last_message_at')


class MessageCreateSerializer(serializers.Serializer):
    """Serializer for creating messages via REST API."""
    other_user_id = serializers.UUIDField()
    text = serializers.CharField(max_length=2000, required=False, allow_blank=True)
    message_type = serializers.ChoiceField(
        choices=['text', 'image', 'location', 'file', 'audio'],
        default='text'
    )
    attachment_url = serializers.URLField(required=False, allow_blank=True)


class VoiceMessageUploadSerializer(serializers.Serializer):
    """Serializer for uploading voice messages."""
    other_user_id = serializers.UUIDField()
    audio_file = serializers.FileField()
    audio_duration = serializers.FloatField(min_value=0.5, max_value=300)  # 0.5s to 5 minutes
    
    def validate_audio_file(self, value):
        """Validate audio file."""
        # Check file size (max 5MB)
        max_size = 5 * 1024 * 1024  # 5MB
        if value.size > max_size:
            raise serializers.ValidationError(f"File size must be less than 5MB. Got {value.size / 1024 / 1024:.1f}MB")
        
        # Check file extension
        valid_extensions = ['.mp3', '.m4a', '.wav', '.ogg', '.flac', '.aac']
        filename = value.name.lower()
        if not any(filename.endswith(ext) for ext in valid_extensions):
            raise serializers.ValidationError(f"Supported formats: {', '.join(valid_extensions)}")
        
        return value
