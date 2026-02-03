# Voice Messages - Documentación

Los mensajes de voz están totalmente integrados en el sistema de chat existente en Django Channels.

## Características

- ✅ Envío de mensajes de voz en tiempo real (WebSocket)
- ✅ Almacenamiento local de archivos de audio
- ✅ REST API para upload de archivos
- ✅ WebSocket para streaming de voz
- ✅ Soporte para múltiples formatos: MP3, M4A, WAV, OGG, FLAC, AAC
- ✅ Límite de 5MB por archivo
- ✅ Duración máxima de 5 minutos
- ✅ Historial persistente

## Endpoints REST

### 1. Obtener lista de salas de chat
```bash
GET /api/chats/chat-rooms/
Authorization: Bearer <firebase_token>
```

### 2. Iniciar/obtener chat con otro usuario
```bash
POST /api/chats/chat-rooms/start-chat/
Authorization: Bearer <firebase_token>
Content-Type: application/json

{
  "other_user_id": "uuid-del-otro-usuario"
}
```

Response:
```json
{
  "id": "uuid",
  "room_name": "chat_uuid1_uuid2",
  "participant_1": {...},
  "participant_2": {...},
  "messages": [...],
  "created_at": "2025-02-03T...",
  "last_message_at": "2025-02-03T..."
}
```

### 3. Enviar mensaje de voz (REST)
```bash
POST /api/chats/chat-rooms/{room_id}/send-voice/
Authorization: Bearer <firebase_token>
Content-Type: multipart/form-data

- audio_file: <archivo_audio>
- audio_duration: 12.5  (en segundos)
```

Response:
```json
{
  "id": "uuid",
  "sender": {...},
  "text": null,
  "message_type": "audio",
  "attachment_url": null,
  "audio_file": "/media/voice_messages/2025/02/03/audio_xxxxx.mp3",
  "audio_duration": 12.5,
  "is_read": false,
  "timestamp": "2025-02-03T12:34:56Z"
}
```

### 4. Obtener mensajes de un chat
```bash
GET /api/chats/chat-rooms/{room_id}/messages/?page=1&page_size=50
Authorization: Bearer <firebase_token>
```

## WebSocket - Mensajes de Voz

### Conectar
```javascript
const roomName = 'chat_user1_id_user2_id';
const socket = new WebSocket(`ws://localhost:8000/ws/chat/${roomName}/`);
```

### Enviar mensaje de voz vía WebSocket
```javascript
// Opción 1: Si ya tienes la URL del archivo subido
socket.send(JSON.stringify({
  type: 'voice_message',
  audio_url: 'https://example.com/media/voice_messages/2025/02/03/audio.mp3',
  audio_duration: 12.5
}));
```

### Recibir mensaje de voz
```javascript
socket.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  if (data.type === 'voice_message') {
    console.log('Mensaje de voz recibido:', {
      message_id: data.data.message_id,
      sender: data.data.sender_email,
      audio_url: data.data.audio_url,
      duration: data.data.audio_duration,
      timestamp: data.data.timestamp
    });
    
    // Reproducir audio
    const audio = new Audio(data.data.audio_url);
    audio.play();
  }
};
```

## Formatos de Mensajes

### Enviar Mensaje de Voz (WebSocket)
```json
{
  "type": "voice_message",
  "audio_url": "https://example.com/media/voice_messages/2025/02/03/audio.mp3",
  "audio_duration": 12.5
}
```

### Recibir Mensaje de Voz (WebSocket)
```json
{
  "type": "voice_message",
  "data": {
    "message_id": "uuid",
    "sender_id": "uuid",
    "sender_email": "user@example.com",
    "audio_url": "https://example.com/media/voice_messages/2025/02/03/audio.mp3",
    "audio_duration": 12.5,
    "timestamp": "2025-02-03T12:34:56Z"
  }
}
```

## Flujo Completo: Cliente Subiendo Mensaje de Voz

### Paso 1: Grabar audio
```javascript
const mediaRecorder = new MediaRecorder(stream);
const audioChunks = [];

mediaRecorder.addEventListener('dataavailable', event => {
  audioChunks.push(event.data);
});

mediaRecorder.addEventListener('stop', async () => {
  const audioBlob = new Blob(audioChunks, { type: 'audio/mp3' });
  await uploadVoiceMessage(audioBlob);
});

mediaRecorder.start();
// ... usuario grabando ...
mediaRecorder.stop();
```

### Paso 2: Subir archivo vía REST
```javascript
async function uploadVoiceMessage(audioBlob) {
  const formData = new FormData();
  formData.append('audio_file', audioBlob, 'voice.mp3');
  formData.append('audio_duration', 12.5);  // en segundos
  
  const response = await fetch(`/api/chats/chat-rooms/${roomId}/send-voice/`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${firebaseToken}`
    },
    body: formData
  });
  
  const message = await response.json();
  console.log('Mensaje de voz enviado:', message);
}
```

### Paso 3: Notificar vía WebSocket (opcional)
```javascript
// Si quieres notificar a través de WebSocket también
socket.send(JSON.stringify({
  type: 'voice_message',
  audio_url: message.audio_file,
  audio_duration: message.audio_duration
}));
```

## Validaciones

| Campo | Min | Max | Formato |
|-------|-----|-----|---------|
| Duración | 0.5 seg | 5 min (300 seg) | Float |
| Tamaño archivo | - | 5 MB | Bytes |
| Formatos | - | - | MP3, M4A, WAV, OGG, FLAC, AAC |

## Almacenamiento

Los archivos se guardan en:
```
media/
└── voice_messages/
    └── 2025/
        └── 02/
            └── 03/
                └── audio_xxxxx.mp3
```

Puedes cambiar esto configurando `MEDIA_ROOT` y `MEDIA_URL` en `settings.py`.

## Escalabilidad: Migrar a S3

Para producción, migra a AWS S3:

1. Instala: `pip install boto3 django-storages`

2. Configura en `settings.py`:
```python
if os.environ.get('USE_S3'):
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'us-east-1')
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
```

## Modelo de Base de Datos

```python
class Message(models.Model):
    id: UUID
    room: ForeignKey(ChatRoom)
    sender: ForeignKey(BaseUser)
    text: TextField (nullable)
    message_type: CharField (choices: text, image, location, file, audio)
    attachment_url: URLField (nullable)
    audio_file: FileField (nullable) -> 'voice_messages/%Y/%m/%d/'
    audio_duration: FloatField (nullable) -> segundos
    is_read: BooleanField
    timestamp: DateTime
```

## Próximas Mejoras

- [ ] Transcripción automática de voz a texto (Google Speech-to-Text, Whisper)
- [ ] Compresión de audio automática
- [ ] Streaming de audio en tiempo real (WebRTC)
- [ ] Soporte para video messages
- [ ] Descarga de mensajes de voz
- [ ] Duración de reproducción parcial
