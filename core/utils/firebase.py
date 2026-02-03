"""Firebase authentication utilities."""

import os
import logging
from typing import Optional, Dict, Any

try:
    import firebase_admin
    from firebase_admin import credentials, auth
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False

logger = logging.getLogger(__name__)


class FirebaseService:
    """Service for Firebase token verification and user management."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._initialize()
            self._initialized = True
    
    def _initialize(self):
        """Initialize Firebase Admin SDK."""
        if not FIREBASE_AVAILABLE:
            logger.warning("Firebase Admin SDK not available. Auth will be disabled.")
            self.app = None
            return
        
        # Try to get Firebase credentials from environment
        creds_path = os.environ.get('FIREBASE_CREDENTIALS_PATH')
        project_id = os.environ.get('FIREBASE_PROJECT_ID')
        
        try:
            if creds_path and os.path.exists(creds_path):
                cred = credentials.Certificate(creds_path)
                self.app = firebase_admin.initialize_app(cred)
                logger.info("Firebase initialized with credentials file")
            elif project_id:
                # Use default credentials (e.g., from GOOGLE_APPLICATION_CREDENTIALS env var)
                options = {'projectId': project_id}
                self.app = firebase_admin.initialize_app(options=options)
                logger.info("Firebase initialized with default credentials")
            else:
                logger.warning("Firebase credentials not configured")
                self.app = None
        except ValueError:
            # Firebase app already initialized
            self.app = firebase_admin.get_app()
        except Exception as e:
            logger.error(f"Failed to initialize Firebase: {e}")
            self.app = None
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify Firebase ID token.
        
        Args:
            token: Firebase ID token
            
        Returns:
            Decoded token dict with user info, or None if verification fails
        """
        if not FIREBASE_AVAILABLE or not self.app:
            logger.warning("Firebase not available, skipping token verification")
            return None
        
        try:
            decoded_token = auth.verify_id_token(token)
            return decoded_token
        except auth.InvalidIdTokenError:
            logger.warning(f"Invalid ID token")
            return None
        except auth.ExpiredIdTokenError:
            logger.warning(f"Expired ID token")
            return None
        except Exception as e:
            logger.error(f"Token verification error: {e}")
            return None
    
    def get_user(self, uid: str) -> Optional[Dict[str, Any]]:
        """
        Get Firebase user by UID.
        
        Args:
            uid: Firebase user UID
            
        Returns:
            User record dict, or None if not found
        """
        if not FIREBASE_AVAILABLE or not self.app:
            return None
        
        try:
            user_record = auth.get_user(uid)
            return {
                'uid': user_record.uid,
                'email': user_record.email,
                'display_name': user_record.display_name,
                'photo_url': user_record.photo_url,
            }
        except auth.UserNotFoundError:
            logger.warning(f"User not found: {uid}")
            return None
        except Exception as e:
            logger.error(f"Error getting user: {e}")
            return None
    
    def create_custom_token(self, uid: str) -> Optional[str]:
        """
        Create custom Firebase token for a user.
        
        Args:
            uid: Firebase user UID
            
        Returns:
            Custom token string, or None if creation fails
        """
        if not FIREBASE_AVAILABLE or not self.app:
            return None
        
        try:
            token = auth.create_custom_token(uid)
            return token.decode('utf-8') if isinstance(token, bytes) else token
        except Exception as e:
            logger.error(f"Error creating custom token: {e}")
            return None


def get_firebase_service() -> FirebaseService:
    """Get singleton Firebase service instance."""
    return FirebaseService()


class FirebaseAuthentication:
    """Django REST Framework authentication class using Firebase."""
    
    def authenticate(self, request):
        """
        Authenticate request using Firebase ID token from Authorization header.
        
        Args:
            request: Django request object
            
        Returns:
            (user, auth) tuple or None if no authentication is provided
            
        Raises:
            AuthenticationFailed: If token is invalid
        """
        from rest_framework.exceptions import AuthenticationFailed
        from users.models import BaseUser
        
        # Get authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION', '').split()
        
        if not auth_header or len(auth_header) != 2 or auth_header[0] != 'Bearer':
            return None
        
        token = auth_header[1]
        firebase_service = get_firebase_service()
        decoded_token = firebase_service.verify_token(token)
        
        if not decoded_token:
            raise AuthenticationFailed('Invalid or expired Firebase token')
        
        uid = decoded_token.get('uid')
        email = decoded_token.get('email')
        
        try:
            user = BaseUser.objects.get(firebase_uid=uid)
        except BaseUser.DoesNotExist:
            # Create user if doesn't exist
            user = BaseUser.objects.create(
                firebase_uid=uid,
                email=email,
                name=decoded_token.get('name', ''),
            )
        
        return (user, token)
    
    def authenticate_header(self, request):
        """Return authentication header."""
        return 'Bearer'
