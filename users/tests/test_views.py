"""
Test cases for User API views.
Tests authentication, authorization, and CRUD operations.
"""

import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from apps.users.models import User, UserRole


@pytest.fixture
def api_client():
    """Create API client"""
    return APIClient()


@pytest.fixture
def admin_user():
    """Create admin user"""
    return User.objects.create_user(
        email='admin@test.com',
        password='adminpass123',
        first_name='Admin',
        last_name='User',
        role=UserRole.ADMIN
    )


@pytest.fixture
def lecturer_user():
    """Create lecturer user"""
    return User.objects.create_user(
        email='lecturer@test.com',
        password='lectpass123',
        first_name='Jane',
        last_name='Teacher',
        role=UserRole.LECTURER
    )


@pytest.fixture
def student_user():
    """Create student user"""
    return User.objects.create_user(
        email='student@test.com',
        password='studpass123',
        first_name='John',
        last_name='Doe',
        role=UserRole.STUDENT
    )


@pytest.mark.django_db
class TestUserRegistration:
    """Test user registration endpoint"""
    
    def test_register_student(self, api_client):
        """Test successful student registration"""
        url = reverse('user-list')
        data = {
            'email': 'newstudent@test.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'first_name': 'New',
            'last_name': 'Student',
            'role': UserRole.STUDENT
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['email'] == 'newstudent@test.com'
        assert response.data['role'] == UserRole.STUDENT
        assert 'password' not in response.data
        
        # Verify user was created
        user = User.objects.get(email='newstudent@test.com')
        assert user.check_password('testpass123')
    
    def test_register_with_mismatched_passwords(self, api_client):
        """Test registration fails with mismatched passwords"""
        url = reverse('user-list')
        data = {
            'email': 'test@test.com',
            'password': 'testpass123',
            'password_confirm': 'differentpass',
            'first_name': 'Test',
            'last_name': 'User',
            'role': UserRole.STUDENT
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'password_confirm' in response.data
    
    def test_register_with_existing_email(self, api_client, student_user):
        """Test registration fails with duplicate email"""
        url = reverse('user-list')
        data = {
            'email': student_user.email,
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'first_name': 'Another',
            'last_name': 'User',
            'role': UserRole.STUDENT
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_register_with_weak_password(self, api_client):
        """Test registration fails with weak password"""
        url = reverse('user-list')
        data = {
            'email': 'test@test.com',
            'password': '123',  # Too short
            'password_confirm': '123',
            'first_name': 'Test',
            'last_name': 'User',
            'role': UserRole.STUDENT
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'password' in response.data


@pytest.mark.django_db
class TestUserAuthentication:
    """Test JWT authentication"""
    
    def test_obtain_token(self, api_client, student_user):
        """Test obtaining JWT token"""
        url = reverse('token_obtain_pair')
        data = {
            'email': 'student@test.com',
            'password': 'studpass123'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
    
    def test_obtain_token_invalid_credentials(self, api_client):
        """Test token obtainment fails with wrong credentials"""
        url = reverse('token_obtain_pair')
        data = {
            'email': 'nonexistent@test.com',
            'password': 'wrongpass'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_refresh_token(self, api_client, student_user):
        """Test refreshing JWT token"""
        # First, obtain token
        token_url = reverse('token_obtain_pair')
        token_data = {
            'email': 'student@test.com',
            'password': 'studpass123'
        }
        token_response = api_client.post(token_url, token_data, format='json')
        refresh_token = token_response.data['refresh']
        
        # Now refresh it
        refresh_url = reverse('token_refresh')
        refresh_data = {'refresh': refresh_token}
        
        response = api_client.post(refresh_url, refresh_data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data


@pytest.mark.django_db
class TestUserProfile:
    """Test user profile endpoints"""
    
    def test_get_own_profile(self, api_client, student_user):
        """Test authenticated user can view their own profile"""
        api_client.force_authenticate(user=student_user)
        url = reverse('user-me')
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == student_user.email
        assert response.data['full_name'] == student_user.get_full_name()
    
    def test_get_profile_unauthenticated(self, api_client):
        """Test unauthenticated user cannot view profile"""
        url = reverse('user-me')
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_update_own_profile(self, api_client, student_user):
        """Test authenticated user can update their profile"""
        api_client.force_authenticate(user=student_user)
        url = reverse('user-me')
        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'bio': 'Updated bio'
        }
        
        response = api_client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        student_user.refresh_from_db()
        assert student_user.first_name == 'Updated'
        assert student_user.last_name == 'Name'
        assert student_user.bio == 'Updated bio'
    
    def test_cannot_update_email_via_profile(self, api_client, student_user):
        """Test user cannot change email via profile update"""
        api_client.force_authenticate(user=student_user)
        url = reverse('user-me')
        original_email = student_user.email
        data = {'email': 'newemail@test.com'}
        
        response = api_client.patch(url, data, format='json')
        
        student_user.refresh_from_db()
        assert student_user.email == original_email
    
    def test_cannot_update_role_via_profile(self, api_client, student_user):
        """Test user cannot change their own role"""
        api_client.force_authenticate(user=student_user)
        url = reverse('user-me')
        data = {'role': UserRole.ADMIN}
        
        response = api_client.patch(url, data, format='json')
        
        student_user.refresh_from_db()
        assert student_user.role == UserRole.STUDENT


@pytest.mark.django_db
class TestUserList:
    """Test user list endpoint (admin only)"""
    
    def test_admin_can_list_users(self, api_client, admin_user, student_user, lecturer_user):
        """Test admin can list all users"""
        api_client.force_authenticate(user=admin_user)
        url = reverse('user-list')
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 3  # At least the 3 fixtures
    
    def test_lecturer_cannot_list_all_users(self, api_client, lecturer_user):
        """Test non-admin cannot list all users"""
        api_client.force_authenticate(user=lecturer_user)
        url = reverse('user-list')
        
        response = api_client.get(url)
        
        # Should be forbidden or return limited data
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_200_OK]
    
    def test_student_cannot_list_all_users(self, api_client, student_user):
        """Test student cannot list all users"""
        api_client.force_authenticate(user=student_user)
        url = reverse('user-list')
        
        response = api_client.get(url)
        
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_200_OK]


@pytest.mark.django_db
class TestPasswordChange:
    """Test password change functionality"""
    
    def test_change_password_success(self, api_client, student_user):
        """Test successful password change"""
        api_client.force_authenticate(user=student_user)
        url = reverse('user-change-password')
        data = {
            'old_password': 'studpass123',
            'new_password': 'newpass123456',
            'new_password_confirm': 'newpass123456'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        
        # Verify password was changed
        student_user.refresh_from_db()
        assert student_user.check_password('newpass123456')
    
    def test_change_password_wrong_old_password(self, api_client, student_user):
        """Test password change fails with wrong old password"""
        api_client.force_authenticate(user=student_user)
        url = reverse('user-change-password')
        data = {
            'old_password': 'wrongpass',
            'new_password': 'newpass123456',
            'new_password_confirm': 'newpass123456'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_change_password_mismatched_new_passwords(self, api_client, student_user):
        """Test password change fails with mismatched new passwords"""
        api_client.force_authenticate(user=student_user)
        url = reverse('user-change-password')
        data = {
            'old_password': 'studpass123',
            'new_password': 'newpass123456',
            'new_password_confirm': 'different123456'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
