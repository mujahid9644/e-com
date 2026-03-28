# ============================================
# USER VIEWS/VIEWSETS
# ============================================
# API views for user authentication and profile management.

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from apps.users.models import Address, UserPreferences
from apps.users.serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserUpdateSerializer,
    AddressSerializer,
    UserPreferencesSerializer
)
import requests
from decouple import config

User = get_user_model()

# ============================================
# USER AUTHENTICATION VIEWSET
# ============================================
class UserAuthViewSet(viewsets.ViewSet):
    """
    API endpoints for user authentication (login, register, logout).
    """
    
    permission_classes = [permissions.AllowAny]
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        """
        Register a new user.
        
        POST /api/auth/register/
        Body: {email, username, password, password_confirm}
        """
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserProfileSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        """
        Login user and return JWT tokens.
        
        POST /api/auth/login/
        Body: {email, password}
        """
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserProfileSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def logout(self, request):
        """
        Logout user (token invalidation on client side).
        
        POST /api/auth/logout/
        """
        return Response({'detail': 'Logout successful'})
    
    @action(detail=False, methods=['post'])
    def google_login(self, request):
        """
        Google OAuth login handler.
        
        POST /api/auth/google_login/
        Body: {access_token}
        """
        access_token = request.data.get('access_token')
        id_token = request.data.get('id_token')

        if not access_token and not id_token:
            return Response(
                {'error': 'id_token or access_token is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            google_data = None

            if id_token:
                # Verify ID token with Google Token Info endpoint
                url = 'https://oauth2.googleapis.com/tokeninfo'
                params = {'id_token': id_token}
                response = requests.get(url, params=params)

                if response.status_code != 200:
                    return Response(
                        {'error': 'Invalid id_token'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                google_data = response.json()
            else:
                # Verify access token with Google userinfo endpoint
                url = 'https://www.googleapis.com/oauth2/v1/userinfo'
                params = {'access_token': access_token}
                response = requests.get(url, params=params)

                if response.status_code != 200:
                    return Response(
                        {'error': 'Invalid access_token'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                google_data = response.json()

            email = google_data.get('email')
            first_name = google_data.get('given_name') or google_data.get('first_name', '')
            last_name = google_data.get('family_name') or google_data.get('last_name', '')

            if not email:
                return Response(
                    {'error': 'Google account email is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            username_base = email.split('@')[0]
            username = username_base
            counter = 1
            while User.objects.filter(username=username).exclude(email=email).exists():
                username = f"{username_base}{counter}"
                counter += 1

            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': username,
                    'first_name': first_name,
                    'last_name': last_name,
                    'is_active': True,
                }
            )

            # If existing user has a blank username update it
            if not user.username:
                user.username = username
                user.save(update_fields=['username'])

            refresh = RefreshToken.for_user(user)

            return Response({
                'user': UserProfileSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                },
                'is_new_user': created
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


# ============================================
# USER PROFILE VIEWSET
# ============================================
class UserProfileViewSet(viewsets.ViewSet):
    """
    API endpoints for user profile management.
    """
    
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Get current authenticated user's profile.
        
        GET /api/auth/profile/me/
        """
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        """
        Update current user's profile information.
        
        PUT/PATCH /api/auth/profile/update_profile/
        """
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(UserProfileSerializer(request.user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """
        Change user password.
        
        POST /api/auth/profile/change_password/
        Body: {old_password, new_password, new_password_confirm}
        """
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        new_password_confirm = request.data.get('new_password_confirm')
        
        # Validate old password
        if not request.user.check_password(old_password):
            return Response(
                {'detail': 'Old password is incorrect.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate new passwords match
        if new_password != new_password_confirm:
            return Response(
                {'detail': 'New passwords do not match.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Set new password
        request.user.set_password(new_password)
        request.user.save()
        
        return Response({'detail': 'Password changed successfully.'})


# ============================================
# ADDRESS VIEWSET
# ============================================
class AddressViewSet(viewsets.ModelViewSet):
    """
    API endpoints for managing user addresses (CRUD).
    """
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AddressSerializer
    
    def get_queryset(self):
        """Get only current user's addresses"""
        return Address.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Create address for current user"""
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def set_as_default(self, request, pk=None):
        """
        Set an address as default.
        
        POST /api/auth/addresses/{id}/set_as_default/
        """
        address = self.get_object()
        # Remove default from other addresses of same type
        Address.objects.filter(
            user=request.user,
            address_type=address.address_type,
            is_default=True
        ).update(is_default=False)
        # Set this as default
        address.is_default = True
        address.save()
        return Response({'detail': 'Address set as default.'})


# ============================================
# USER PREFERENCES VIEWSET
# ============================================
class UserPreferencesViewSet(viewsets.ViewSet):
    """
    API endpoints for user preferences and settings.
    """
    
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def get_preferences(self, request):
        """
        Get current user's preferences.
        
        GET /api/auth/preferences/get_preferences/
        """
        try:
            preferences = request.user.preferences
        except UserPreferences.DoesNotExist:
            preferences = UserPreferences.objects.create(user=request.user)
        
        serializer = UserPreferencesSerializer(preferences)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put', 'patch'])
    def update_preferences(self, request):
        """
        Update user preferences.
        
        PUT/PATCH /api/auth/preferences/update_preferences/
        """
        try:
            preferences = request.user.preferences
        except UserPreferences.DoesNotExist:
            preferences = UserPreferences.objects.create(user=request.user)
        
        serializer = UserPreferencesSerializer(preferences, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
