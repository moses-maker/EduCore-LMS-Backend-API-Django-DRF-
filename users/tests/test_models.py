"""
Test cases for User models.
Demonstrates TDD approach for model testing.
"""

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from apps.users.models import User, UserRole, UserManager


@pytest.mark.django_db
class TestUserManager:
    """Test custom user manager"""
    
    def test_create_user(self):
        """Test creating a regular user"""
        user = User.objects.create_user(
            email='student@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe'
        )
        
        assert user.email == 'student@test.com'
        assert user.first_name == 'John'
        assert user.last_name == 'Doe'
        assert user.role == UserRole.STUDENT
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False
        assert user.check_password('testpass123')
    
    def test_create_user_without_email(self):
        """Test creating user without email raises error"""
        with pytest.raises(ValueError, match='Users must have an email address'):
            User.objects.create_user(
                email='',
                password='testpass123'
            )
    
    def test_create_superuser(self):
        """Test creating a superuser"""
        admin = User.objects.create_superuser(
            email='admin@test.com',
            password='adminpass123',
            first_name='Admin',
            last_name='User'
        )
        
        assert admin.email == 'admin@test.com'
        assert admin.role == UserRole.ADMIN
        assert admin.is_active is True
        assert admin.is_staff is True
        assert admin.is_superuser is True
        assert admin.check_password('adminpass123')
    
    def test_email_normalization(self):
        """Test email is normalized on creation"""
        user = User.objects.create_user(
            email='Test@EXAMPLE.COM',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
        assert user.email == 'Test@example.com'


@pytest.mark.django_db
class TestUserModel:
    """Test User model"""
    
    def test_user_string_representation(self):
        """Test user __str__ method"""
        user = User.objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe'
        )
        
        expected = 'John Doe (test@test.com)'
        assert str(user) == expected
    
    def test_get_full_name(self):
        """Test get_full_name method"""
        user = User.objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe'
        )
        
        assert user.get_full_name() == 'John Doe'
    
    def test_get_short_name(self):
        """Test get_short_name method"""
        user = User.objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe'
        )
        
        assert user.get_short_name() == 'John'
    
    def test_unique_email_constraint(self):
        """Test email uniqueness constraint"""
        User.objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe'
        )
        
        with pytest.raises(IntegrityError):
            User.objects.create_user(
                email='test@test.com',
                password='anotherpass123',
                first_name='Jane',
                last_name='Smith'
            )
    
    def test_role_properties(self):
        """Test role property methods"""
        student = User.objects.create_user(
            email='student@test.com',
            password='pass123',
            first_name='Student',
            last_name='One',
            role=UserRole.STUDENT
        )
        
        lecturer = User.objects.create_user(
            email='lecturer@test.com',
            password='pass123',
            first_name='Lecturer',
            last_name='One',
            role=UserRole.LECTURER
        )
        
        admin = User.objects.create_user(
            email='admin@test.com',
            password='pass123',
            first_name='Admin',
            last_name='One',
            role=UserRole.ADMIN
        )
        
        # Test student
        assert student.is_student is True
        assert student.is_lecturer is False
        assert student.is_admin is False
        
        # Test lecturer
        assert lecturer.is_student is False
        assert lecturer.is_lecturer is True
        assert lecturer.is_admin is False
        
        # Test admin
        assert admin.is_student is False
        assert admin.is_lecturer is False
        assert admin.is_admin is True
    
    def test_user_ordering(self):
        """Test users are ordered by date_joined descending"""
        user1 = User.objects.create_user(
            email='user1@test.com',
            password='pass123',
            first_name='User',
            last_name='One'
        )
        
        user2 = User.objects.create_user(
            email='user2@test.com',
            password='pass123',
            first_name='User',
            last_name='Two'
        )
        
        users = list(User.objects.all())
        assert users[0] == user2
        assert users[1] == user1
    
    def test_user_profile_fields(self):
        """Test user profile fields"""
        user = User.objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            phone_number='+1234567890',
            bio='Test bio'
        )
        
        assert user.phone_number == '+1234567890'
        assert user.bio == 'Test bio'
        assert user.profile_picture.name == ''  # No picture uploaded


@pytest.mark.django_db
class TestUserRoles:
    """Test user role functionality"""
    
    def test_default_role_is_student(self):
        """Test default role is STUDENT"""
        user = User.objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
        assert user.role == UserRole.STUDENT
    
    def test_can_create_lecturer(self):
        """Test creating a lecturer user"""
        lecturer = User.objects.create_user(
            email='lecturer@test.com',
            password='testpass123',
            first_name='Jane',
            last_name='Teacher',
            role=UserRole.LECTURER
        )
        
        assert lecturer.role == UserRole.LECTURER
        assert lecturer.is_lecturer is True
    
    def test_can_create_admin(self):
        """Test creating an admin user"""
        admin = User.objects.create_user(
            email='admin@test.com',
            password='testpass123',
            first_name='Admin',
            last_name='User',
            role=UserRole.ADMIN
        )
        
        assert admin.role == UserRole.ADMIN
        assert admin.is_admin is True


@pytest.mark.django_db
class TestUserAuthentication:
    """Test user authentication features"""
    
    def test_password_hashing(self):
        """Test passwords are properly hashed"""
        password = 'testpass123'
        user = User.objects.create_user(
            email='test@test.com',
            password=password,
            first_name='Test',
            last_name='User'
        )
        
        # Password should not be stored in plain text
        assert user.password != password
        # Should be able to verify password
        assert user.check_password(password) is True
        # Wrong password should fail
        assert user.check_password('wrongpass') is False
    
    def test_last_login_tracking(self):
        """Test last_login is tracked"""
        user = User.objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
        assert user.last_login is None
        
        # Simulate login by setting last_login
        from django.utils import timezone
        user.last_login = timezone.now()
        user.save()
        
        assert user.last_login is not None
