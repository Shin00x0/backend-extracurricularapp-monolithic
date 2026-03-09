# Plan de Implementación - Backend Extracurricular App

## Resumen General
Este documento establece el orden de implementación, testing y validación de cada módulo del backend monolítico.

Cada módulo debe completar las siguientes fases:
1. ✅ **Implementación**: Desarrollar modelos, serializers, views, URLs
2. ✅ **Testing Unitario**: Crear y ejecutar tests de funcionalidad
3. ✅ **Testing REST**: Validar endpoints con Postman/colecciones

---

## 1. MÓDULO: Users

### 1.1 Implementación
- [ ] Revisar modelo User en `users/models.py`
- [ ] Validar serializers en `users/serializers.py`
- [ ] Implementar vistas (CRUD) en `users/views.py`
- [ ] Configurar URLs en `users/urls.py`
- [ ] Registrar en admin `users/admin.py`
- [ ] Implementar login local para admins en `/admin/login/` usando `LocalAuthBackend` (session/JWT)
- [ ] Implementar endpoint `/api/users/sync-firebase/` para sincronización / webhook desde Firebase (manual + webhook)

### 1.2 Testing Unitario
- [ ] Crear tests en `users/tests.py`
- [ ] Test: Creación de usuario
- [ ] Test: Autenticación
- [ ] Test: Validación de campos
- [ ] Test: Permisos y roles
- [ ] Ejecutar: `python manage.py test users`

### 1.3 Testing REST (Postman)
- [ ] POST `/api/users/register/` - Crear usuario
- [ ] POST `/api/users/login/` - Autenticación
- [ ] GET `/api/users/profile/` - Obtener perfil
- [ ] PUT `/api/users/profile/` - Actualizar perfil
- [ ] GET `/api/users/{id}/` - Obtener usuario por ID
- [ ] DELETE `/api/users/{id}/` - Eliminar usuario
- [ ] Validar tokens JWT
- [ ] Documentar colección en Postman

---

## 2. MÓDULO: Clients

### 2.1 Implementación
- [ ] Revisar modelo Client en `clients/models.py`
- [ ] Validar serializers en `clients/serializers.py`
- [ ] Implementar vistas (CRUD) en `clients/views.py`
- [ ] Configurar URLs en `clients/urls.py`
- [ ] Registrar en admin `clients/admin.py`
- [ ] Relación con Users

### 2.2 Testing Unitario
- [ ] Crear tests en `clients/tests.py`
- [ ] Test: Creación de cliente
- [ ] Test: Validación de datos
- [ ] Test: Relación con usuarios
- [ ] Test: Filtrado y búsqueda
- [ ] Ejecutar: `python manage.py test clients`

### 2.3 Testing REST (Postman)
- [ ] POST `/api/clients/` - Crear cliente
- [ ] GET `/api/clients/` - Listar clientes
- [ ] GET `/api/clients/{id}/` - Obtener cliente
- [ ] PUT `/api/clients/{id}/` - Actualizar cliente
- [ ] DELETE `/api/clients/{id}/` - Eliminar cliente
- [ ] GET `/api/clients/?search=` - Búsqueda
- [ ] Validar paginación

---

## 3. MÓDULO: Workers

### 3.1 Implementación
- [ ] Revisar modelo Worker en `workers/models.py`
- [ ] Validar serializers en `workers/serializers.py`
- [ ] Implementar vistas (CRUD) en `workers/views.py`
- [ ] Configurar URLs en `workers/urls.py`
- [ ] Registrar en admin `workers/admin.py`
- [ ] Relación con Users

### 3.2 Testing Unitario
- [ ] Crear tests en `workers/tests.py`
- [ ] Test: Creación de trabajador
- [ ] Test: Validación de especialidad
- [ ] Test: Disponibilidad
- [ ] Test: Calificaciones
- [ ] Ejecutar: `python manage.py test workers`

### 3.3 Testing REST (Postman)
- [ ] POST `/api/workers/` - Crear trabajador
- [ ] GET `/api/workers/` - Listar trabajadores
- [ ] GET `/api/workers/{id}/` - Obtener trabajador
- [ ] PUT `/api/workers/{id}/` - Actualizar trabajador
- [ ] DELETE `/api/workers/{id}/` - Eliminar trabajador
- [ ] GET `/api/workers/available/` - Filtrar disponibles
- [ ] GET `/api/workers/by-specialty/` - Filtrar por especialidad

---

## 4. MÓDULO: Work Requests

### 4.1 Implementación
- [ ] Revisar modelo WorkRequest en `work_requests/models.py`
- [ ] Validar serializers en `work_requests/serializers.py`
- [ ] Implementar vistas (CRUD) en `work_requests/views.py`
- [ ] Configurar URLs en `work_requests/urls.py`
- [ ] Registrar en admin `work_requests/admin.py`
- [ ] Relaciones con Users, Clients, Workers

### 4.2 Testing Unitario
- [ ] Crear tests en `work_requests/tests.py`
- [ ] Test: Creación de solicitud
- [ ] Test: Cambios de estado
- [ ] Test: Validación de fechas
- [ ] Test: Asignación de trabajador
- [ ] Ejecutar: `python manage.py test work_requests`

### 4.3 Testing REST (Postman)
- [ ] POST `/api/work-requests/` - Crear solicitud
- [ ] GET `/api/work-requests/` - Listar solicitudes
- [ ] GET `/api/work-requests/{id}/` - Obtener solicitud
- [ ] PUT `/api/work-requests/{id}/` - Actualizar solicitud
- [ ] DELETE `/api/work-requests/{id}/` - Eliminar solicitud
- [ ] PATCH `/api/work-requests/{id}/assign/` - Asignar trabajador
- [ ] PATCH `/api/work-requests/{id}/status/` - Cambiar estado
- [ ] Validar filtros por estado, fecha, cliente

---

## 5. MÓDULO: Interactions

### 5.1 Implementación
- [ ] Revisar modelo Interaction en `interactions/models.py`
- [ ] Validar serializers en `interactions/serializers.py`
- [ ] Implementar vistas en `interactions/views.py`
- [ ] Configurar URLs en `interactions/urls.py`
- [ ] Registrar en admin `interactions/admin.py`

### 5.2 Testing Unitario
- [ ] Crear tests en `interactions/tests.py`
- [ ] Test: Registro de interacción
- [ ] Test: Timestamps
- [ ] Test: Relaciones
- [ ] Ejecutar: `python manage.py test interactions`

### 5.3 Testing REST (Postman)
- [ ] POST `/api/interactions/` - Crear interacción
- [ ] GET `/api/interactions/` - Listar interacciones
- [ ] GET `/api/interactions/{id}/` - Obtener interacción
- [ ] GET `/api/interactions/by-user/` - Historial de usuario
- [ ] GET `/api/interactions/by-worker/` - Historial de trabajador

---

## 6. MÓDULO: Messaging

### 6.1 Implementación
- [ ] Revisar modelo Message en `messaging/models.py`
- [ ] Validar serializers en `messaging/serializers.py`
- [ ] Implementar vistas en `messaging/views.py`
- [ ] Configurar URLs en `messaging/urls.py`
- [ ] Registrar en admin `messaging/admin.py`

### 6.2 Testing Unitario
- [ ] Crear tests en `messaging/tests.py`
- [ ] Test: Envío de mensaje
- [ ] Test: Lectura de mensajes
- [ ] Test: Validación de contenido
- [ ] Ejecutar: `python manage.py test messaging`

### 6.3 Testing REST (Postman)
- [ ] POST `/api/messages/` - Enviar mensaje
- [ ] GET `/api/messages/` - Listar mensajes
- [ ] GET `/api/messages/{id}/` - Obtener mensaje
- [ ] GET `/api/messages/conversation/` - Conversación entre usuarios
- [ ] PUT `/api/messages/{id}/` - Actualizar mensaje (marcar como leído)
- [ ] DELETE `/api/messages/{id}/` - Eliminar mensaje

---

## 7. MÓDULO: Chats (Real-time WebSocket)

### 7.1 Implementación
- [ ] Revisar modelo Chat en `chats/models.py`
- [ ] Validar serializers en `chats/serializers.py`
- [ ] Implementar vistas en `chats/views.py`
- [ ] Configurar URLs en `chats/urls.py`
- [ ] Configurar consumers WebSocket en `chats/consumers.py`
- [ ] Configurar routing en `chats/routing.py`
- [ ] Registrar en admin `chats/admin.py`

### 7.2 Testing Unitario
- [ ] Crear tests en `chats/tests.py`
- [ ] Test: Creación de chat
- [ ] Test: Mensajes en tiempo real
- [ ] Test: Notificaciones
- [ ] Ejecutar: `python manage.py test chats`

### 7.3 Testing REST/WebSocket (Postman + WebSocket Client)
- [ ] POST `/api/chats/` - Crear chat
- [ ] GET `/api/chats/` - Listar chats
- [ ] GET `/api/chats/{id}/` - Obtener chat
- [ ] GET `/api/chats/{id}/messages/` - Obtener mensajes del chat
- [ ] WebSocket: `ws://localhost:8000/ws/chat/{id}/` - Conexión en tiempo real
- [ ] WebSocket: Enviar mensaje
- [ ] WebSocket: Recibir mensaje
- [ ] WebSocket: Notificaciones de usuario conectado/desconectado

---

## 8. MÓDULO: Storage

### 8.1 Implementación
- [ ] Revisar modelo Storage en `storage/models.py`
- [ ] Validar serializers en `storage/serializers.py`
- [ ] Implementar vistas en `storage/views.py`
- [ ] Configurar URLs en `storage/urls.py`
- [ ] Registrar en admin `storage/admin.py`
- [ ] Configurar almacenamiento (S3 o local)

### 8.2 Testing Unitario
- [ ] Crear tests en `storage/tests.py`
- [ ] Test: Subida de archivo
- [ ] Test: Descarga de archivo
- [ ] Test: Validación de tipo
- [ ] Test: Permisos
- [ ] Ejecutar: `python manage.py test storage`

### 8.3 Testing REST (Postman)
- [ ] POST `/api/storage/upload/` - Subir archivo
- [ ] GET `/api/storage/{id}/` - Obtener archivo
- [ ] GET `/api/storage/{id}/download/` - Descargar archivo
- [ ] DELETE `/api/storage/{id}/` - Eliminar archivo
- [ ] GET `/api/storage/` - Listar archivos
- [ ] Validar tamaños y tipos de archivo

---

## 9. MÓDULO: Stats

### 9.1 Implementación
- [ ] Revisar modelo Stats en `stats/models.py`
- [ ] Validar serializers en `stats/serializers.py`
- [ ] Implementar vistas en `stats/views.py`
- [ ] Configurar URLs en `stats/urls.py`
- [ ] Registrar en admin `stats/admin.py`

### 9.2 Testing Unitario
- [ ] Crear tests en `stats/tests.py`
- [ ] Test: Cálculo de estadísticas
- [ ] Test: Agregación de datos
- [ ] Ejecutar: `python manage.py test stats`

### 9.3 Testing REST (Postman)
- [ ] GET `/api/stats/users/` - Estadísticas de usuarios
- [ ] GET `/api/stats/workers/` - Estadísticas de trabajadores
- [ ] GET `/api/stats/work-requests/` - Estadísticas de solicitudes
- [ ] GET `/api/stats/performance/` - Rendimiento general
- [ ] GET `/api/stats/monthly/` - Estadísticas mensuales
- [ ] GET `/api/stats/by-category/` - Por categoría

---

## Checklist General

### Antes de Iniciar
- [ ] Entorno virtual activado: `venv_win\Scripts\activate`
- [ ] Dependencias instaladas: `pip install -r requirements.txt`
- [ ] Base de datos configurada: `python manage.py migrate`
- [ ] Servidor ejecutándose: `python manage.py runserver`

### Durante Implementación
- [ ] Código limpio y comentado
- [ ] Validaciones implementadas
- [ ] Manejo de errores
- [ ] Logs configurados

### Testing
- [ ] Cobertura mínima 80%
- [ ] Todos los tests pasan
- [ ] Edge cases cubiertos

### Documentación
- [ ] Docstrings en funciones
- [ ] Colección Postman actualizada
- [ ] README de endpoints

---

## Herramientas Necesarias

| Herramienta | Uso | Instalación |
|-------------|-----|-------------|
| Python 3.x | Desarrollo | Ya instalado |
| Django | Framework | `pip install django` |
| Django REST Framework | API REST | `pip install djangorestframework` |
| Postman | Testing REST | [Descargar](https://www.postman.com/) |
| Git | Control versión | Ya configurado |
| SQLite | Base datos | Ya configurado |

---

## Notas Importantes

1. **Orden de Implementación**: Seguir el orden presentado respetando dependencias
2. **Testing Obligatorio**: No pasar a siguiente módulo sin tests pasando
3. **Postman**: Exportar colecciones después de validar cada módulo
4. **Migraciones**: Ejecutar `python manage.py makemigrations && python manage.py migrate` después de cambios en modelos
5. **Documentación**: Mantener actualizado durante desarrollo

---

## Estados de Progreso

### Módulo: Users
**Progreso General**: 0% ❌
- Implementación: ❌
- Testing Unitario: ❌
- Testing REST: ❌

### Módulo: Clients
**Progreso General**: 0% ❌
- Implementación: ❌
- Testing Unitario: ❌
- Testing REST: ❌

### Módulo: Workers
**Progreso General**: 0% ❌
- Implementación: ❌
- Testing Unitario: ❌
- Testing REST: ❌

### Módulo: Work Requests
**Progreso General**: 0% ❌
- Implementación: ❌
- Testing Unitario: ❌
- Testing REST: ❌

### Módulo: Interactions
**Progreso General**: 0% ❌
- Implementación: ❌
- Testing Unitario: ❌
- Testing REST: ❌

### Módulo: Messaging
**Progreso General**: 0% ❌
- Implementación: ❌
- Testing Unitario: ❌
- Testing REST: ❌

### Módulo: Chats (WebSocket)
**Progreso General**: 0% ❌
- Implementación: ❌
- Testing Unitario: ❌
- Testing REST: ❌

### Módulo: Storage
**Progreso General**: 0% ❌
- Implementación: ❌
- Testing Unitario: ❌
- Testing REST: ❌

### Módulo: Stats
**Progreso General**: 0% ❌
- Implementación: ❌
- Testing Unitario: ❌
- Testing REST: ❌

---

**Última actualización**: Febrero 3, 2026
