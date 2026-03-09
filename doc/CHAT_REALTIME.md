# Django Channels - Real-time Chat Implementation

Esta implementación proporciona un sistema de chat en tiempo real usando Django Channels y WebSockets.

## Características

- ✅ Chat en tiempo real (WebSocket)
- ✅ Múltiples usuarios conectados simultáneamente
- ✅ Historial de mensajes persistente
- ✅ Indicadores de escritura (typing indicator)
- ✅ Recibos de lectura (read receipts)
- ✅ Soporte para múltiples tipos de mensajes (texto, imagen, ubicación, archivo)
- ✅ Autenticación con Firebase
- ✅ Layer Redis para producción

## Instalación

### Dependencias Instaladas
```bash
pip install channels daphne channels-redis
```

### Configuración Django

1. **settings.py** - Agregado:
   - `ASGI_APPLICATION = 'core.asgi.application'`
   - `CHANNEL_LAYERS` (Redis o InMemory)
   - `daphne` y `channels` en INSTALLED_APPS

2. **asgi.py** - Configurado:
   - ProtocolTypeRouter para HTTP + WebSocket
   - AuthMiddlewareStack para autenticación
   - URLRouter con rutas WebSocket

3. **chats/routing.py** - Rutas WebSocket:
   ```python
   ws/chat/<room_name>/  ->  ChatConsumer
   ```

## Uso

### 1. WebSocket - Cliente JavaScript

```javascript
// Conectarse a la sala de chat
const roomName = 'chat_user1_id_user2_id'; // IDs de usuarios ordenados
const socket = new WebSocket(`ws://localhost:8000/ws/chat/${roomName}/`);

// Enviar mensaje
socket.send(JSON.stringify({
  type: 'chat_message',
  message: 'Hola!',
  message_type: 'text',
  attachment_url: null
}));

// Enviar indicador de escritura
socket.send(JSON.stringify({
  type: 'typing',
  is_typing: true
}));

// Enviar recibo de lectura
socket.send(JSON.stringify({
  type: 'read_receipt',
  message_id: 'message-uuid'
}));

// Recibir mensajes
socket.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Mensaje recibido:', data);
};
```

### 2. REST API - Listar Chat Rooms

```bash
GET /api/v1/chat-rooms/
Authorization: Bearer <firebase_token>
```

Response:
```json
[
  {
    "id": "uuid",
    "participant_1": {...},
    "participant_2": {...},
    "created_at": "2025-02-03T...",
    "last_message_at": "2025-02-03T...",
    "last_message": {...},
    "unread_count": 3
  }
]
```

### 3. REST API - Detalle Chat Room

```bash
GET /api/v1/chat-rooms/<room_id>/
Authorization: Bearer <firebase_token>
```

## Modelos de Datos

### ChatRoom
```python
- id: UUID
- participant_1: ForeignKey(BaseUser)
- participant_2: ForeignKey(BaseUser)
- created_at: DateTime
- last_message_at: DateTime (nullable)
- room_name: Propiedad calculada para WebSocket
```

### Message
```python
- id: UUID
- room: ForeignKey(ChatRoom)
- sender: ForeignKey(BaseUser)
- text: TextField
- message_type: CharField (text, image, location, file)
- attachment_url: URLField (nullable)
- is_read: BooleanField
- timestamp: DateTime
```

## Formatos de Mensajes WebSocket

### Enviar Mensaje
```json
{
  "type": "chat_message",
  "message": "Contenido del mensaje",
  "message_type": "text",
  "attachment_url": null
}
```

### Recibir Mensaje
```json
{
  "type": "chat_message",
  "data": {
    "message_id": "uuid",
    "sender_id": "uuid",
    "sender_email": "user@example.com",
    "text": "Contenido del mensaje",
    "message_type": "text",
    "attachment_url": null,
    "timestamp": "2025-02-03T12:34:56Z"
  }
}
```

### Indicador de Escritura
```json
{
  "type": "typing",
  "is_typing": true
}
```

### Recibir Indicador
```json
{
  "type": "typing_indicator",
  "data": {
    "user_id": "uuid",
    "user_email": "user@example.com",
    "is_typing": true
  }
}
```

### Recibo de Lectura
```json
{
  "type": "read_receipt",
  "message_id": "uuid"
}
```

### Recibir Recibo
```json
{
  "type": "message_read",
  "data": {
    "message_id": "uuid",
    "reader_id": "uuid"
  }
}
```

## Ejecutar el Servidor

### Desarrollo
```bash
# Con Daphne (ASGI)
python manage.py runserver

# O específicamente con Daphne
daphne -b 0.0.0.0 -p 8000 core.asgi:application
```

### Producción
```bash
# Con Daphne y múltiples workers
daphne -b 0.0.0.0 -p 8000 -w 4 core.asgi:application
```

## Redis (Producción)

Para usar Redis en lugar de InMemory:

1. **Instalar Redis**
```bash
brew install redis  # macOS
# o
apt-get install redis-server  # Linux
```

2. **Iniciar Redis**
```bash
redis-server
```

3. **Configuración automática**
La app detecta Redis y lo usa automáticamente. Si no está disponible, usa InMemory.

## Autenticación

El WebSocket usa `AuthMiddlewareStack` que:
1. Extrae el token Bearer del header HTTP
2. Autentica al usuario con Firebase
3. Asocia el usuario a la conexión WebSocket

En los Consumers se puede acceder a `self.user` para obtener el usuario autenticado.

## Seguridad

- ✅ Autenticación requerida para WebSocket
- ✅ Solo puedes enviar mensajes en salas donde eres participante
- ✅ Los usuarios no autenticados son desconectados automáticamente
- ✅ Los mensajes se almacenan en la BD con referencias de usuario

## Próximas Mejoras

- [ ] Crear grupo de chat para múltiples usuarios
- [ ] Notificaciones push con FCM
- [ ] Búsqueda de mensajes
- [ ] Reacciones a mensajes (emojis)
- [ ] Edición y eliminación de mensajes
- [ ] Menciones (@user)
- [ ] Encriptación end-to-end
