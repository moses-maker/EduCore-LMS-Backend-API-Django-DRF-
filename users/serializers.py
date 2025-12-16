"""
User serializers for EduCore LMS.
"""

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from apps.users.models import User, UserRole


class UserSerializer(serializers.ModelSerializer):
    """Standard user serializer"""
    
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'full_name',
            'role', 'phone_number', 'bio', 'profile_picture',
            'is_active', 'date_joined', 'last_login'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = [
            'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'role',
            'phone_number', 'bio'
        ]
    
    def validate(self, attrs):
        """Validate password confirmation"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': 'Passwords do not match'
            })
        return attrs
    
    def validate_role(self, value):
        """Ensure only valid roles can be self-registered"""
        # Typically, only students should self-register
        # Admins create lecturer and admin accounts
        if value not in [UserRole.STUDENT, UserRole.LECTURER]:
            raise serializers.ValidationError(
                'Invalid role for registration'
            )
        return value
    
    def create(self, validated_data):
        """Create user with hashed password"""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        user = User.objects.create_user(
            password=password,
            **validated_data
        )
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for user profile updates"""
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone_number',
            'bio', 'profile_picture'
        ]


class PasswordChangeSerializer(serializers.Serializer):
    """Serializer for password change"""
    
    old_password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    new_password_confirm = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    
    def validate(self, attrs):
        """Validate password change"""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({
                'new_password_confirm': 'Passwords do not match'
            })
        return attrs
    
    def validate_old_password(self, value):
        """Verify old password"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Incorrect password')
        return value


class UserListSerializer(serializers.ModelSerializer):
    """Minimal serializer for user lists"""
    
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'role', 'is_active']
