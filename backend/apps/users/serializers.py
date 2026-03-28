# ============================================
# USER SERIALIZERS
# ============================================
# Serialize user data for API responses.

from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from apps.users.models import Address, UserPreferences

User = get_user_model()

# ============================================
# USER REGISTRATION SERIALIZER
# ============================================
class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Accepts email, username, password and creates a new user.
    """
    
    # Confirm password field (not in model)
    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        help_text='Confirm password'
    )
    
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 
                  'password', 'password_confirm']
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},
        }
    
    def validate(self, attrs):
        """Validate passwords match"""
        if attrs['password'] != attrs.pop('password_confirm'):
            raise serializers.ValidationError({
                'password': 'Passwords do not match.'
            })
        return attrs
    
    def create(self, validated_data):
        """Create user with hashed password"""
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            password=validated_data['password']
        )
        return user


# ============================================
# USER LOGIN SERIALIZER
# ============================================
class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    Authenticates user and returns JWT tokens.
    """
    
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        """Authenticate user"""
        email = attrs.get('email')
        password = attrs.get('password')
        
        # Try to get user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid email or password.')
        
        # Authenticate
        user = authenticate(username=user.username, password=password)
        if not user:
            raise serializers.ValidationError('Invalid email or password.')
        
        attrs['user'] = user
        return attrs


# ============================================
# USER PROFILE SERIALIZER
# ============================================
class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile information.
    Used for displaying user details.
    """
    
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name',
                  'phone_number', 'date_of_birth', 'profile_picture',
                  'is_verified_email', 'is_verified_phone', 'is_staff', 'is_superuser', 'created_at']
        read_only_fields = ['id', 'created_at', 'is_verified_email', 'is_verified_phone', 'is_staff', 'is_superuser']


# ============================================
# USER UPDATE SERIALIZER
# ============================================
class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile.
    """
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 
                  'date_of_birth', 'profile_picture']


# ============================================
# ADDRESS SERIALIZER
# ============================================
class AddressSerializer(serializers.ModelSerializer):
    """
    Serializer for user addresses.
    """
    
    class Meta:
        model = Address
        fields = ['id', 'full_name', 'phone', 'street_address', 'city',
                  'state_or_province', 'postal_code', 'country',
                  'delivery_instructions', 'is_default', 'address_type']
        read_only_fields = ['id']


# ============================================
# USER PREFERENCES SERIALIZER
# ============================================
class UserPreferencesSerializer(serializers.ModelSerializer):
    """
    Serializer for user preferences and settings.
    """
    
    class Meta:
        model = UserPreferences
        fields = ['email_notifications_enabled', 'sms_notifications_enabled',
                  'marketing_emails_enabled', 'dark_mode_enabled', 
                  'language', 'currency']
