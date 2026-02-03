"""WebSocket consumers for real-time chat functionality."""

import json
import logging
from typing import Optional
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from users.models import BaseUser
from .models import ChatRoom, Message

logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for real-time chat messaging."""
    
    async def connect(self):
        """Handle WebSocket connection."""
        # Extract room_name from URL route
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope['user']
        
        # Validate user authentication
        if not self.user.is_authenticated:
            await self.close()
            return
        
        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        logger.info(f"User {self.user.email} connected to {self.room_name}")
        
        # Notify other users that this user joined
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_join',
                'user_id': str(self.user.id),
                'user_email': self.user.email,
            }
        )
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
        logger.info(f"User {self.user.email} disconnected from {self.room_name}")
        
        # Notify other users that this user left
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_leave',
                'user_id': str(self.user.id),
                'user_email': self.user.email,
            }
        )
    
    async def receive(self, text_data):
        """Handle incoming WebSocket message."""
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            if message_type == 'chat_message':
                await self.handle_chat_message(data)
            elif message_type == 'voice_message':
                await self.handle_voice_message(data)
            elif message_type == 'typing':
                await self.handle_typing(data)
            elif message_type == 'read_receipt':
                await self.handle_read_receipt(data)
            else:
                logger.warning(f"Unknown message type: {message_type}")
        except json.JSONDecodeError:
            logger.error("Invalid JSON received")
            await self.send_error("Invalid message format")
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            await self.send_error(str(e))
    
    async def handle_chat_message(self, data):
        """Process and broadcast chat message."""
        message_text = data.get('message', '').strip()
        message_type = data.get('message_type', 'text')
        attachment_url = data.get('attachment_url')
        
        if not message_text and not attachment_url:
            await self.send_error("Message cannot be empty")
            return
        
        # Save message to database
        message = await self.save_message(
            message_text,
            message_type,
            attachment_url
        )
        
        if not message:
            await self.send_error("Failed to save message")
            return
        
        # Broadcast message to all users in the room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message_id': str(message['id']),
                'sender_id': str(message['sender_id']),
                'sender_email': message['sender_email'],
                'text': message['text'],
                'message_type': message['message_type'],
                'attachment_url': message['attachment_url'],
                'timestamp': message['timestamp'],
            }
        )
    
    async def handle_voice_message(self, data):
        """Process and broadcast voice message."""
        audio_url = data.get('audio_url')
        audio_duration = data.get('audio_duration', 0)
        
        if not audio_url:
            await self.send_error("audio_url is required")
            return
        
        if not (0.5 <= audio_duration <= 300):
            await self.send_error("Audio duration must be between 0.5 and 300 seconds")
            return
        
        # Save message to database
        message = await self.save_voice_message(audio_url, audio_duration)
        
        if not message:
            await self.send_error("Failed to save voice message")
            return
        
        # Broadcast message to all users in the room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'voice_message',
                'message_id': str(message['id']),
                'sender_id': str(message['sender_id']),
                'sender_email': message['sender_email'],
                'audio_url': message['audio_url'],
                'audio_duration': message['audio_duration'],
                'timestamp': message['timestamp'],
            }
        )
    
    async def handle_typing(self, data):
        """Broadcast typing indicator."""
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'typing_indicator',
                'user_id': str(self.user.id),
                'user_email': self.user.email,
                'is_typing': data.get('is_typing', True),
            }
        )
    
    async def handle_read_receipt(self, data):
        """Mark messages as read."""
        message_id = data.get('message_id')
        await self.mark_message_as_read(message_id)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'message_read',
                'message_id': message_id,
                'reader_id': str(self.user.id),
            }
        )
    
    # Event handlers (receive from group_send)
    
    async def chat_message(self, event):
        """Send chat message to WebSocket."""
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'data': {
                'message_id': event['message_id'],
                'sender_id': event['sender_id'],
                'sender_email': event['sender_email'],
                'text': event['text'],
                'message_type': event['message_type'],
                'attachment_url': event['attachment_url'],
                'timestamp': event['timestamp'],
            }
        }))
    
    async def voice_message(self, event):
        """Send voice message to WebSocket."""
        await self.send(text_data=json.dumps({
            'type': 'voice_message',
            'data': {
                'message_id': event['message_id'],
                'sender_id': event['sender_id'],
                'sender_email': event['sender_email'],
                'audio_url': event['audio_url'],
                'audio_duration': event['audio_duration'],
                'timestamp': event['timestamp'],
            }
        }))
    
    async def typing_indicator(self, event):
        """Send typing indicator to WebSocket."""
        # Don't send typing indicator to the user who is typing
        if event['user_id'] != str(self.user.id):
            await self.send(text_data=json.dumps({
                'type': 'typing_indicator',
                'data': {
                    'user_id': event['user_id'],
                    'user_email': event['user_email'],
                    'is_typing': event['is_typing'],
                }
            }))
    
    async def message_read(self, event):
        """Send read receipt to WebSocket."""
        await self.send(text_data=json.dumps({
            'type': 'message_read',
            'data': {
                'message_id': event['message_id'],
                'reader_id': event['reader_id'],
            }
        }))
    
    async def user_join(self, event):
        """Notify user joined."""
        # Don't send join notification to the user who joined
        if event['user_id'] != str(self.user.id):
            await self.send(text_data=json.dumps({
                'type': 'user_join',
                'data': {
                    'user_id': event['user_id'],
                    'user_email': event['user_email'],
                }
            }))
    
    async def user_leave(self, event):
        """Notify user left."""
        await self.send(text_data=json.dumps({
            'type': 'user_leave',
            'data': {
                'user_id': event['user_id'],
                'user_email': event['user_email'],
            }
        }))
    
    async def send_error(self, error_message: str):
        """Send error message to client."""
        await self.send(text_data=json.dumps({
            'type': 'error',
            'data': {
                'message': error_message,
            }
        }))
    
    # Database operations
    
    @database_sync_to_async
    def save_message(self, text: str, message_type: str, attachment_url: Optional[str] = None) -> Optional[dict]:
        """Save message to database."""
        try:
            # Get or create chat room
            room = self.get_or_create_room()
            if not room:
                return None
            
            # Create message
            message = Message.objects.create(
                room=room,
                sender=self.user,
                text=text,
                message_type=message_type,
                attachment_url=attachment_url,
            )
            
            # Update room's last_message_at
            room.last_message_at = message.timestamp
            room.save(update_fields=['last_message_at'])
            
            return {
                'id': message.id,
                'sender_id': message.sender.id,
                'sender_email': message.sender.email,
                'text': message.text,
                'message_type': message.message_type,
                'attachment_url': message.attachment_url,
                'timestamp': message.timestamp.isoformat(),
            }
        except Exception as e:
            logger.error(f"Error saving message: {e}")
            return None
    
    @database_sync_to_async
    def save_voice_message(self, audio_url: str, audio_duration: float) -> Optional[dict]:
        """Save voice message to database."""
        try:
            # Get or create chat room
            room = self.get_or_create_room()
            if not room:
                return None
            
            # Create message
            message = Message.objects.create(
                room=room,
                sender=self.user,
                message_type='audio',
                attachment_url=audio_url,
                audio_duration=audio_duration,
            )
            
            # Update room's last_message_at
            room.last_message_at = message.timestamp
            room.save(update_fields=['last_message_at'])
            
            return {
                'id': message.id,
                'sender_id': message.sender.id,
                'sender_email': message.sender.email,
                'audio_url': audio_url,
                'audio_duration': audio_duration,
                'timestamp': message.timestamp.isoformat(),
            }
        except Exception as e:
            logger.error(f"Error saving voice message: {e}")
            return None
    
    @database_sync_to_async
    def mark_message_as_read(self, message_id: str) -> bool:
        """Mark message as read."""
        try:
            message = Message.objects.get(id=message_id)
            if not message.is_read:
                message.is_read = True
                message.save(update_fields=['is_read'])
            return True
        except Message.DoesNotExist:
            logger.warning(f"Message not found: {message_id}")
            return False
        except Exception as e:
            logger.error(f"Error marking message as read: {e}")
            return False
    
    def get_or_create_room(self) -> Optional[ChatRoom]:
        """Get or create chat room based on room_name."""
        try:
            # room_name format: chat_user1_id_user2_id (sorted)
            parts = self.room_name.split('_')
            if len(parts) != 3 or parts[0] != 'chat':
                logger.error(f"Invalid room name format: {self.room_name}")
                return None
            
            user_ids = [parts[1], parts[2]]
            
            # Get both users
            users = BaseUser.objects.filter(id__in=user_ids)
            if users.count() != 2:
                logger.error(f"Could not find both users for room: {self.room_name}")
                return None
            
            user1, user2 = sorted(users, key=lambda u: str(u.id))
            
            # Get or create room
            room, _ = ChatRoom.objects.get_or_create(
                participant_1=user1,
                participant_2=user2,
            )
            return room
        except Exception as e:
            logger.error(f"Error getting or creating room: {e}")
            return None
