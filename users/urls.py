"""URLs for users app."""

from django.urls import path
import views
app_name = 'users'

urlpatterns = [
    # Auth endpoints will be added here
    # GET /api/v1/auth/verify
    # GET /api/v1/users/:userId
    # PUT /api/v1/users/:userId
    # POST /api/v1/users/avatar
    
    # User profile endpoints
    path('profile/', views.UserProfileDetailView.as_view(), name='user-profile'),
    path('profile/update/', views.UserProfileUpdateView.as_view(), name='user-profile-update'),
    path('<str:user_id>/', views.UserPublicProfileView.as_view(), name='user-public-profile'),
    
    # Avatar endpoints
    path('avatar/upload/', views.AvatarUploadView.as_view(), name='avatar-upload'),
    
    # Device token endpoints
    path('device-token/register/', views.DeviceTokenRegisterView.as_view(), name='device-token-register'),
]
